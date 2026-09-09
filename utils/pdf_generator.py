from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
def report_pdf(title, lines):
    buf=BytesIO(); c=canvas.Canvas(buf,pagesize=letter); y=760
    c.setFont("Helvetica-Bold",16); c.drawString(45,y,title); y-=35; c.setFont("Helvetica",10)
    for line in lines:
        for chunk in [str(line)[i:i+100] for i in range(0,len(str(line)),100)]:
            if y<45: c.showPage(); c.setFont("Helvetica",10); y=760
            c.drawString(45,y,chunk); y-=16
    c.save(); return buf.getvalue()
