from pathlib import Path
import textwrap
import fitz
from PIL import Image, ImageChops
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).parent
source = Path(r"C:\Users\alesz\Downloads\cloudops-01-monitoring-guide.pdf")
appendix = ROOT / "cli-appendix.pdf"
output = ROOT / "cloudops-01-monitoring-guide-formatted.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Sub", parent=styles["BodyText"], fontSize=12, leading=15, textColor="#455a64"))
styles.add(ParagraphStyle(name="H", parent=styles["Heading2"], fontSize=13, leading=15, textColor="#17365d", spaceBefore=6, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontSize=17, leading=21, textColor="#17365d", spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name="CodeX", parent=styles["Code"], fontName="Courier", fontSize=7.4, leading=9.2, leftIndent=0, rightIndent=0, textColor="#263238", spaceAfter=0))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontSize=9.5, leading=12.5, spaceAfter=6))

def p(text):
    return Paragraph(text.replace("&", "&amp;"), styles["BodyX"])

story = [Paragraph("AWS CLI Equivalent", styles["Title"]), Paragraph("CloudOps 01 monitoring and incident response", styles["Sub"]), p("This appendix preserves the original guide and adds the complete PowerShell CLI repeat. Use a dedicated sandbox profile and us-east-1. Do not paste credentials into files."), Spacer(1, 8)]
sections = [
    ("1. Configure and verify the profile", "aws configure sso\naws sso login --profile YOUR_PROFILE\naws sts get-caller-identity --profile YOUR_PROFILE"),
    ("2. Set variables", '$Profile = "YOUR_PROFILE"\n$Region = "us-east-1"\n$FunctionName = "cloudops-01-monitoring"\n$LogGroup = "/aws/lambda/$FunctionName"\n$RoleName = "$FunctionName-execution-role"\n$AlarmName = "$FunctionName-errors"\n$AccountId = aws sts get-caller-identity --profile $Profile --query Account --output text'),
    ("3. Create logs and IAM", 'aws logs create-log-group --log-group-name $LogGroup --region $Region --profile $Profile\naws logs put-retention-policy --log-group-name $LogGroup --retention-in-days 1 --region $Region --profile $Profile\n\nCreate trust-policy.json for lambda.amazonaws.com, then run:\naws iam create-role --role-name $RoleName --assume-role-policy-document file://trust-policy.json --profile $Profile\naws iam put-role-policy --role-name $RoleName --policy-name "$FunctionName-logging" --policy-document file://logging-policy.json --profile $Profile\nStart-Sleep -Seconds 10'),
    ("4. Package and deploy", 'Compress-Archive -Path labs/cloudops/01-monitoring-incidents/src/lambda_function.py -DestinationPath cloudops-01-monitoring.zip -Force\n$RoleArn = aws iam get-role --role-name $RoleName --query Role.Arn --output text --profile $Profile\naws lambda create-function --function-name $FunctionName --runtime python3.12 --handler lambda_function.lambda_handler --role $RoleArn --zip-file fileb://cloudops-01-monitoring.zip --memory-size 128 --timeout 3 --region $Region --profile $Profile'),
    ("5. Invoke success and failure", '"{\"fail\": false}" | Set-Content success.json\n"{\"fail\": true}" | Set-Content failure.json\naws lambda invoke --function-name $FunctionName --payload fileb://success.json --cli-binary-format raw-in-base64-out success-response.json --region $Region --profile $Profile\naws lambda invoke --function-name $FunctionName --payload fileb://failure.json --cli-binary-format raw-in-base64-out failure-response.json --region $Region --profile $Profile\n# Run the failure invocation three times.'),
    ("6. Create and inspect the alarm", 'aws cloudwatch put-metric-alarm --alarm-name $AlarmName --namespace AWS/Lambda --metric-name Errors --dimensions Name=FunctionName,Value=$FunctionName --statistic Sum --period 60 --evaluation-periods 1 --datapoints-to-alarm 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --region $Region --profile $Profile\n\naws cloudwatch describe-alarms --alarm-names $AlarmName --query "MetricAlarms[0].[AlarmName,StateValue,MetricName,Namespace,Threshold]" --output table --region $Region --profile $Profile'),
    ("7. Inspect logs and recover", 'aws logs tail $LogGroup --since 30m --format short --region $Region --profile $Profile\n# Invoke success.json three times, then wait for one-minute evaluation.\naws cloudwatch describe-alarms --alarm-names $AlarmName --query "MetricAlarms[0].[AlarmName,StateValue,StateReason]" --output table --region $Region --profile $Profile'),
    ("8. Clean up", 'aws cloudwatch delete-alarms --alarm-names $AlarmName --region $Region --profile $Profile\naws lambda delete-function --function-name $FunctionName --region $Region --profile $Profile\naws logs delete-log-group --log-group-name $LogGroup --region $Region --profile $Profile\naws iam delete-role-policy --role-name $RoleName --policy-name "$FunctionName-logging" --profile $Profile\naws iam delete-role --role-name $RoleName --profile $Profile'),
    ("9. Terraform equivalent", 'Create a separate lab directory and state. Do not reuse the enterprise infra root or a production backend.\n\nterraform {\n  required_providers {\n    aws = { source = "hashicorp/aws", version = "~> 5.0" }\n    archive = { source = "hashicorp/archive", version = "~> 2.4" }\n  }\n}\n\nprovider "aws" {\n  region = "us-east-1"\n}\n\nvariable "function_name" { default = "cloudops-01-monitoring" }\n\nresource "aws_cloudwatch_log_group" "lab" {\n  name              = "/aws/lambda/${var.function_name}"\n  retention_in_days = 1\n}\n\ndata "archive_file" "lambda" {\n  type        = "zip"\n  source_file = "../src/lambda_function.py"\n  output_path = "${path.module}/lambda.zip"\n}\n\nresource "aws_iam_role" "lambda" {\n  name = "${var.function_name}-execution-role"\n  assume_role_policy = jsonencode({Version="2012-10-17", Statement=[{Effect="Allow", Principal={Service="lambda.amazonaws.com"}, Action="sts:AssumeRole"}]})\n}\n\nresource "aws_iam_role_policy" "logs" {\n  role = aws_iam_role.lambda.id\n  policy = jsonencode({Version="2012-10-17", Statement=[{Effect="Allow", Action=["logs:CreateLogStream", "logs:PutLogEvents"], Resource="${aws_cloudwatch_log_group.lab.arn}:*"}]})\n}\n\nresource "aws_lambda_function" "lab" {\n  function_name    = var.function_name\n  role             = aws_iam_role.lambda.arn\n  runtime          = "python3.12"\n  handler          = "lambda_function.lambda_handler"\n  filename         = data.archive_file.lambda.output_path\n  source_code_hash = data.archive_file.lambda.output_base64sha256\n  memory_size     = 128\n  timeout         = 3\n  depends_on      = [aws_cloudwatch_log_group.lab]\n}\n\nresource "aws_cloudwatch_metric_alarm" "errors" {\n  alarm_name          = "${var.function_name}-errors"\n  namespace           = "AWS/Lambda"\n  metric_name         = "Errors"\n  dimensions          = { FunctionName = aws_lambda_function.lab.function_name }\n  statistic           = "Sum"\n  period              = 60\n  evaluation_periods  = 1\n  datapoints_to_alarm = 1\n  threshold           = 1\n  comparison_operator = "GreaterThanOrEqualToThreshold"\n  treat_missing_data  = "notBreaching"\n}'),
    ("10. Terraform validation and deployment", 'terraform init\nterraform fmt -check\nterraform validate\nterraform plan -out cloudops-01.tfplan\n\nReview the plan, account, region, resource names, IAM policy, public exposure, and estimated cost. Apply only after reviewing the sandbox plan:\n\nterraform apply cloudops-01.tfplan\n\nUse the AWS CLI commands in this appendix to invoke the function and verify the alarm. Terraform provisions resources; it does not replace the failure drill or runtime verification.'),
    ("11. Terraform cleanup", 'terraform plan -destroy -out cloudops-01-destroy.tfplan\n\nReview the destroy plan and confirm it contains only the lab resources, then run:\n\nterraform apply cloudops-01-destroy.tfplan\n\nVerify the log group, alarm, Lambda, role, and policy are gone. Keep Terraform state private and never commit lambda.zip, state files, credentials, or secret values.'),
]
# The CLI appendix ends at cleanup. Terraform is rendered only in the separate
# file-by-file section below; do not duplicate the legacy compact entries here.
sections = [item for item in sections if not item[0].startswith(("9.", "10.", "11."))]
for title, code in sections:
    wrapped = []
    for raw in code.splitlines():
        if not raw:
            wrapped.append(" ")
        else:
            wrapped.extend(textwrap.wrap(raw, width=112, replace_whitespace=False, drop_whitespace=False) or [" "])
    code_rows = [[Paragraph(line.replace("&", "&amp;"), styles["CodeX"])] for line in wrapped]
    block = Table(code_rows, colWidths=[9.65*inch])
    block.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f3f6f8")), ("BOX", (0,0), (-1,-1), .4, colors.HexColor("#c8d0d6")), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
    story += [Paragraph(title, styles["H"]), block, Spacer(1, 4)]
story += [PageBreak(), Paragraph("Terraform section by file", styles["Title"]), Paragraph("The following section is included in this PDF in the requested file-by-file order. It is sourced from terraform-guide.md.", styles["Sub"])]
md_lines = (ROOT / "terraform-guide.md").read_text(encoding="utf-8").splitlines()
md_code = []
md_in_code = False
for line in md_lines:
    if line.startswith("```"):
        if md_in_code:
            wrapped_code = []
            for raw in md_code:
                indent = raw[:len(raw) - len(raw.lstrip())]
                wrapped_code.extend(textwrap.wrap(raw, width=112, replace_whitespace=False, drop_whitespace=False, subsequent_indent=indent + "  ") or [" "])
            block = Table([[Preformatted("\n".join(wrapped_code), styles["CodeX"])]], colWidths=[9.65*inch])
            block.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f3f6f8")), ("BOX", (0,0), (-1,-1), .4, colors.HexColor("#c8d0d6")), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
            story += [block, Spacer(1, 4)]
            md_code = []
            md_in_code = False
        else:
            md_in_code = True
        continue
    if md_in_code:
        md_code.append(line)
    elif line.startswith("## "):
        story.append(Paragraph(line[3:], styles["H"]))
    elif line.startswith("# "):
        story.append(Paragraph(line[2:], styles["H1x"]))
    elif line.strip():
        story.append(Paragraph(line.replace("&", "&amp;"), styles["BodyX"]))
story += [Spacer(1, 8), p("Important: the CloudWatch metric name is Errors. The alarm name is cloudops-01-monitoring-errors. The original guide pages, including their images, are preserved unchanged before this appendix."), PageBreak()]
SimpleDocTemplate(str(appendix), pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=28, bottomMargin=28).build(story)
writer = PdfWriter()
source_doc = fitz.open(str(source))
cropped_pages = {}
for index, source_page in enumerate(source_doc):
    source_text = source_page.get_text()
    if "Handler:" in source_text or "7. Recover and prove it" in source_text:
        pix = source_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        background = Image.new("RGB", image.size, "white")
        bbox = ImageChops.difference(image, background).getbbox()
        if bbox:
            pad = 24
            crop = image.crop((max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(image.width, bbox[2]+pad), min(image.height, bbox[3]+pad)))
            cropped = fitz.open()
            replacement = cropped.new_page(width=source_page.rect.width, height=source_page.rect.height)
            # Insert the crop through a temporary in-memory PNG to preserve quality.
            png = __import__('io').BytesIO()
            crop.save(png, format="PNG")
            replacement.insert_image(replacement.rect, stream=png.getvalue())
            cropped_pages[index] = cropped
for index, page in enumerate(PdfReader(str(source)).pages):
    # The supplied original contains an older AWS CLI appendix starting at
    # the page headed "AWS CLI". Preserve the original guide and evidence
    # pages, but omit that obsolete appendix before adding the corrected one.
    page_text = page.extract_text() or ""
    normalized_text = "".join(page_text.split())
    if "AWSCLI" in normalized_text and "$Profile" in normalized_text:
        break
    if index in cropped_pages:
        replacement_pdf = PdfReader(stream=__import__('io').BytesIO(cropped_pages[index].tobytes()))
        writer.add_page(replacement_pdf.pages[0])
    else:
        writer.add_page(page)
for page in PdfReader(str(appendix)).pages:
    writer.add_page(page)
with output.open("wb") as fh:
    writer.write(fh)
print(output)
