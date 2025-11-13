import os
import sys
from gvm.errors import GvmError  # 使うかもしれないので念のため
from gvm.protocols.gmp import Gmp


def get_env(name, required=True, default=None):
    value = os.environ.get(name, default)
    if required and not value:
        print(f"[エラー] 必須の環境変数 {name} が設定されていません。", file=sys.stderr)
        sys.exit(1)
    return value


def find_config_id(gmp, name):
    print(f"[情報] スキャン設定 '{name}' を検索します。")

    configs_xml = gmp.get_scan_configs()

    nodes = configs_xml.xpath("config") + configs_xml.xpath("scan_config")
    for cfg in nodes:
        node_name = cfg.xpath("name/text()")
        if node_name and node_name[0] == name:
            cfg_id = cfg.get("id")
            print(f"[情報] スキャン設定 '{name}' の ID を発見: {cfg_id}")
            return cfg_id

    print(f"[警告] スキャン設定 '{name}' が見つかりませんでした。")
    return None


def ensure_target(gmp, name, hosts):
    print(f"[情報] ターゲット '{name}' を確認します。hosts={hosts}")

    targets_xml = gmp.get_targets(filter=f"name={name}")
    for tgt in targets_xml.xpath("target"):
        tgt_name = tgt.xpath("name/text()")
        if tgt_name and tgt_name[0] == name:
            tgt_id = tgt.get("id")
            print(f"[情報] 既存ターゲットを利用します: {name} (ID: {tgt_id})")
            return tgt_id

    print(f"[情報] ターゲット '{name}' が存在しないため新規作成します。")
    resp = gmp.create_target(name=name, hosts=hosts)
    new_id = resp.get("id")
    if not new_id:
        print("[エラー] ターゲットの作成に失敗しました。", file=sys.stderr)
        sys.exit(1)
    print(f"[情報] ターゲットを作成しました。ID: {new_id}")
    return new_id


def ensure_task(gmp, name, config_id, target_id):
    print(f"[情報] タスク '{name}' を確認します。")

    tasks_xml = gmp.get_tasks(filter=f"name={name}")
    for task in tasks_xml.xpath("task"):
        task_name = task.xpath("name/text()")
        if task_name and task_name[0] == name:
            task_id = task.get("id")
            print(f"[情報] 既存タスクを利用します: {name} (ID: {task_id})")
            return task_id

    print(f"[情報] タスク '{name}' が存在しないため新規作成します。")
    resp = gmp.create_task(
        name=name,
        config_id=config_id,
        target_id=target_id,
    )
    new_id = resp.get("id")
    if not new_id:
        print("[エラー] タスクの作成に失敗しました。", file=sys.stderr)
        sys.exit(1)
    print(f"[情報] タスクを作成しました。ID: {new_id}")
    return new_id