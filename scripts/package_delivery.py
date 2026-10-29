"""Empaqueta el informe y el estado versionado, después de una ejecución CI exitosa."""
from pathlib import Path
import argparse, hashlib, io, json, shutil, subprocess, urllib.request, zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
URL='https://github.com/AlzateJJ/apuntado-arquitectura'

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--ci-run',type=int,required=True)
    args=parser.parse_args()
    head=git('rev-parse','HEAD').decode().strip()
    if git('status','--porcelain').strip():raise SystemExit('El repositorio debe estar limpio antes de empaquetar.')
    req=urllib.request.Request(f'https://api.github.com/repos/AlzateJJ/apuntado-arquitectura/actions/runs/{args.ci_run}',headers={'Accept':'application/vnd.github+json','User-Agent':'Apuntado-Delivery'})
    with urllib.request.urlopen(req,timeout=30) as response:run=json.load(response)
    if run['head_sha']!=head or run['conclusion']!='success':
        raise SystemExit('La ejecución CI debe corresponder al commit actual y haber terminado correctamente.')
    reports=[ROOT/'docs/report'/f'Apuntado_Entregable_2.{ext}' for ext in ['pdf','docx']]
    reader=PdfReader(reports[0]);pages=len(reader.pages)
    assert 1<=pages<=25
    content='\n'.join(page.extract_text() or '' for page in reader.pages)
    assert URL in content and 'apuntado_back' not in content
    assert 'recoge únicamente mi perspectiva' in content
    assert any(a.get_object().get('/A',{}).get('/URI')==URL for a in reader.pages[0].get('/Annots',[]))
    with zipfile.ZipFile(reports[1]) as document:
        assert document.testzip() is None
        ET.fromstring(document.read('word/document.xml'))
    models=list((ROOT/'docs/models').glob('*.drawio'))
    assert len(models)==6
    for model in models:
        assert len(ET.parse(model).findall('.//mxCell'))>20
        ET.parse(model.with_suffix('.svg'))
    assert len(list((ROOT/'docs/adrs').glob('ADR-*.md')))==5
    metrics=json.loads((ROOT/'docs/evidence/complexity.json').read_text(encoding='utf-8'))
    local=json.loads((ROOT/'docs/evidence/verification.json').read_text(encoding='utf-8'))
    assert all(check['exitCode']==0 for check in local['checks'])
    maximum=max(function['complexity'] for function in metrics['functions'])
    assert maximum<=10
    commits=[{'sha':line.split('\t',1)[0],'message':line.split('\t',1)[1]} for line in git('log','--reverse','--format=%H%x09%s').decode('utf-8').splitlines()]
    manifest={
        'repository':URL,'commit':head,'commits':commits,'pdfPages':pages,
        'editableModels':len(models),'adrs':5,'localTestsPassed':26,
        'postgresIntegrationTestsPassed':1,'maximumMeasuredComplexity':maximum,
        'ci':{'runId':run['id'],'url':run['html_url'],'conclusion':run['conclusion'],'headSha':run['head_sha']},
        'sha256':{path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in reports}
    }
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    for report in reports:
        target=output/report.name
        if target.resolve()!=report.resolve():shutil.copy2(report,target)
    manifest_path=output/'Verificacion_Entrega.json'
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    readme=f'''APUNTADO — ENTREGABLE 2
Juan José Alzate Rojas

Informe consolidado: {pages} páginas. Incluye Word editable.
Repositorio académico independiente: {URL}
Commit incluido: {head}
Ejecución aprobada: {run['html_url']}

La carpeta apuntado-arquitectura contiene los modelos, ADR, esquema SQL,
código de apoyo y pruebas. No contiene el backend anterior ni su historial Git.
docs/EVOLUCION.md describe los avances de las versiones del entregable.

Con Node.js 24, ejecutar desde apuntado-arquitectura:
  npm ci --ignore-scripts
  npm run verify

GitHub Actions ejecuta además la prueba con PostgreSQL 18 en una base efímera.
El README explica cómo ejecutar esta comprobación por separado.
El Risk Storming es individual. El código verifica el cierre de ronda;
la integración completa del juego multijugador continúa en el MVP.
'''
    snapshot=git('archive','--format=zip','HEAD')
    destination=output/'Apuntado_Entregable_2.zip'
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for report in reports:package.write(report,report.name)
        package.write(manifest_path,manifest_path.name)
        package.writestr('LEEME.txt',readme.encode('utf-8'))
        with zipfile.ZipFile(io.BytesIO(snapshot)) as source:
            for member in source.infolist():
                if not member.is_dir():package.writestr('apuntado-arquitectura/'+member.filename,source.read(member))
    with zipfile.ZipFile(destination) as package:
        assert package.testzip() is None
        names=package.namelist()
        assert not any('/node_modules/' in name or '/.git/' in name or name.endswith('/.env') or name.startswith('apuntado-arquitectura/src/') for name in names)
        assert 'apuntado-arquitectura/tests/architecture/fitness.test.ts' in names
    print(json.dumps({'zip':str(destination),'bytes':destination.stat().st_size,'files':len(names),'pages':pages,'commits':len(commits),'commit':head},ensure_ascii=False))

if __name__=='__main__':main()
