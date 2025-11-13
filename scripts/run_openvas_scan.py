import os
from gvm.protocols.gmp import Gmp
from gvm.connections import TLSConnection


def main() -> None:
    """GitHub Actions から呼び出して OpenVAS (gvmd) にスキャンを依頼する最小構成スクリプト。"""

    # --- 環境変数の読み取り ---
    gmp_host = os.environ["GMP_HOST"]
    gmp_port = int(os.environ["GMP_PORT"])
    gmp_user = os.environ["GMP_USER"]
    gmp_password = os.environ["GMP_PASSWORD"]

    base_config_name = os.environ["BASE_CONFIG_NAME"]
    target_hosts = os.environ["TARGET_HOSTS"]
    task_name = os.environ.get("TASK_NAME", "GitHub CI DAST Scan")

    print(f"[INFO] gvmd へ TLS 接続します: {gmp_host}:{gmp_port}")
    connection = TLSConnection(hostname=gmp_host, port=gmp_port)

    # --- gvmd への接続 & 認証 ---
    with Gmp(connection=connection) as gmp:
        print("[INFO] 認証中...")
        gmp.authenticate(gmp_user, gmp_password)
        print("[INFO] gvmd への認証に成功しました。")

        # --- スキャン設定 ID の取得 ---
        print(f"[INFO] スキャン設定 '{base_config_name}' を検索します。")
        configs_xml = gmp.get_configs()
        base_config_id = None

        for cfg in configs_xml.xpath("*/config"):
            name_node = cfg.find("name")
            if name_node is not None and name_node.text == base_config_name:
                base_config_id = cfg.get("id")
                break

        if not base_config_id:
            raise RuntimeError(f"scan config '{base_config_name}' が見つかりませんでした")

        print(f"[INFO] 使用するスキャン設定 ID: {base_config_id}")

        # --- ターゲット作成 ---
        print(f"[INFO] ターゲットを作成します: hosts={target_hosts}")
        target_resp = gmp.create_target(
            name=f"CI target {target_hosts}",
            hosts=[target_hosts],
            port_range="1-65535",
        )
        target_id = target_resp.get("id")
        print(f"[INFO] ターゲット ID: {target_id}")

        # --- タスク作成 ---
        print(f"[INFO] タスク '{task_name}' を作成します。")
        task_resp = gmp.create_task(
            name=task_name,
            config_id=base_config_id,
            target_id=target_id,
        )
        task_id = task_resp.get("id")
        print(f"[INFO] タスク ID: {task_id}")

        # --- スキャン開始 ---
        print("[INFO] スキャンを開始します...")
        start_resp = gmp.start_task(task_id)
        status = start_resp.get("status")
        status_text = start_resp.get("status_text")
        print(f"[INFO] start_task の結果: status={status}, status_text={status_text}")
        print("[INFO] スキャン開始要求を gvmd に送信しました。詳細は OpenVAS/GSA で確認してください。")


if __name__ == "__main__":
    main()