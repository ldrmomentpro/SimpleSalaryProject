import pandas as pd
from io import BytesIO
from flask import send_file

from .utils import calc_age

def generate_excel_report(records):
    data = []
    for r in records:
        data.append({
            "id": r.id,
            "first_name": r.first_name,
            "last_name": r.last_name,
            "email": r.email,
            "phone": r.phone,
            "birth_date": r.birth_date,
            "city": r.city.name if r.city else None,
            "country": r.city.country.name if r.city and r.city.country else None,
            "grade": r.salary_grade.grade if r.salary_grade else None,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        })

    df = pd.DataFrame(data, columns=[
        "id", "first_name", "last_name", "email", "phone",
        "birth_date", "city", "country", "grade", "created_at", "updated_at"
    ])

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output


def download_excel(records, age_param):

    if age_param is not None:
        filtered_records = [r for r in records if calc_age(r.birth_date) >= age_param]
    else:
        filtered_records = records

    output = generate_excel_report(filtered_records)
    return send_file(
        output,
        as_attachment=True,
        download_name="table.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
