from faker import Faker

def production_record(id: int):
    """ダミーの生産実績を生成する"""
    fake = Faker("ja_JP")  
    return {
        "record_id": id,
        "machine_id": f"M-{fake.random_int(1, 50)}",
        "operator": fake.name(),
        "start_time": fake.date_time().isoformat(),
        "end_time": fake.date_time().isoformat(),
        "product_code": f"P-{fake.random_int(1000, 9999)}",
        "quantity": fake.random_int(1, 500),
        "status": fake.random_element(["OK", "NG", "REWORK"]),
    }


# print(f"{production_record()}")