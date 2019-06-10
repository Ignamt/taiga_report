import subprocess

md2docxProcess = subprocess.run(["pandoc", "template_report.md", "-o", 
  "template_report.docx"])

if (md2docxProcess.returncode == 0):
    print("Conversión exitosa.")
else:
    print("Falló la conversión.")
