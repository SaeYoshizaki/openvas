import os
import sys

from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.errors import GvmError

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)


def main():
    gmp_host = get_env("GMP_HOST")
    gmp_port_str = get_env("GMP_PORT")
    gmp_user = get_env("GMP_USER")
    gmp_password = get_env("GMP_PASSWORD")

    base_config_name = get_env("BASE_CONFIG_NAME")
    target_hosts = get_env("TARGET_HOSTS")
    task_name = get_env("TASK_NAME", required=False, default="GitHub CI DAST Scan")

    try:
        gmp_port = int(gmp_port_str)
    except ValueError:
        print(f"[エラー] GMP_PORT の値が不正です: {gmp_port_str}", file=sys.stderr)
        sys.exit(1)

    print(f"[情報] gvmd へ接続します: {gmp_host}:{gmp_port}")

    connection = TLSConnection(hostname=gmp_host, port=gmp_port)

    try:
        with Gmp(connection=connection) as gmp:
            gmp.authenticate(gmp_user, gmp_password)
            print("[情報] gvmd への認証に成功しました。")

            config_id = find_config_id(gmp, base_config_name)
            if not config_id:
                print(
                    f"[エラー] スキャン設定 '{base_config_name}' が見つからなかったため終了します。",
                    file=sys.stderr,
                )
                sys.exit(1)

            target_name = f"CI target {target_hosts}"
            target_id = ensure_target(gmp, target_name, hosts=target_hosts)

            task_id = ensure_task(gmp, task_name, config_id=config_id, target_id=target_id)

            print(f"[情報] タスク '{task_name}' (ID: {task_id}) のスキャンを開始します。")
            start_resp = gmp.start_task(task_id)
            status = start_resp.get("status")
            status_text = start_resp.get("status_text")

            print(f"[情報] start_task の結果: status={status}, status_text={status_text}")
            print("[情報] スキャン開始要求を gvmd に送信しました。詳細は OpenVAS/GSA 側で確認してください。")

    except GvmError as e:
        print(f"[エラー] GVM 関連の例外が発生しました: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[エラー] 予期しない例外が発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()