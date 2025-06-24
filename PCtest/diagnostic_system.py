import pandas as pd
from datetime import datetime
import json
import os

class DiagnosticSystem:
    def __init__(self, csv_path="diagnosis_history.csv"):
        self.csv_path = csv_path
        self.rules = [
            (lambda d: not d["power"] and not d["fans"], "Можливо, несправний блок живлення"),
            (lambda d: d["power"] and not d["fans"] and d["temp"] > 70, "Перегрів системи охолодження"),
            (lambda d: d["power"] and d["fans"] and not d["noise"], "Можливо, не працює накопичувач"),
            (lambda d: d["power"] and d["fans"] and d["temp"] > 90 and d["noise"], "Критичний перегрів")
        ]

    def validate(self, data):
        if "temp" in data:
            try:
                data["temp"] = float(data["temp"])
            except ValueError:
                raise ValueError("Температура повинна бути числом")
        return True

    def diagnose(self, data):
        self.validate(data)
        diagnoses = [diag for cond, diag in self.rules if cond(data)]
        return diagnoses if diagnoses else ["Невідомо"]

    def save_to_csv(self, symptoms, diagnoses):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symptoms": json.dumps(symptoms, ensure_ascii=False),
            "diagnosis": "; ".join(diagnoses)
        }

        df = pd.DataFrame([record])
        if os.path.exists(self.csv_path):
            df.to_csv(self.csv_path, mode='a', index=False, header=False)
        else:
            df.to_csv(self.csv_path, index=False)

    def load_history(self, last_n=10):
        if not os.path.exists(self.csv_path):
            return pd.DataFrame()
        df = pd.read_csv(self.csv_path)
        return df.tail(last_n)
