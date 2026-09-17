import csv
import io


def leads_csv(rows):
    fields = ["id", "name", "category", "location", "email", "phone", "website", "rating", "review_count", "score", "priority", "status", "notes"]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
