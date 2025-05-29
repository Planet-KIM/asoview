import os
import tarfile


def compress_folder(folder_id, base_dir=None):
    try:
        # 압축할 폴더가 위치한 경로 (module/third_party 디렉토리)
        #base_dir = os.path.abspath(os.path.join("./../../modules/third_party/asodesign_cache/"))
        if base_dir==None:
            base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"./../../design_folder/")
        folder_path = os.path.join(base_dir, folder_id)

        # 압축할 폴더가 존재하는지 확인
        if not os.path.exists(folder_path):
            raise FileNotFoundError((1, f"폴더 '{folder_path}'가 존재하지 않습니다."))

        # 출력 파일 경로를 module/third_party 폴더 내에 생성
        output_path = os.path.join(base_dir, f"{folder_id}.tar.gz")
        if os.path.exists(output_path):
            raise Exception((0, f"The file({output_path}) is created."))

        # tarfile 모듈을 사용하여 gzip 압축 방식으로 tar 아카이브 생성
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(folder_path, arcname=folder_id)

        return {"msg": (0, f"압축 파일 '{output_path}'이(가) 생성되었습니다.") }
    except Exception as e:
        print(e.args[0])
        return {'msg': e.args[0] }