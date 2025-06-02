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
            raise FileNotFoundError(f"폴더 '{folder_path}'가 존재하지 않습니다.")

        # 출력 파일 경로를 module/third_party 폴더 내에 생성
        output_path = os.path.join(base_dir, f"{folder_id}.tar.gz")
        if os.path.exists(output_path):
            raise Exception(f"The file({output_path}) is created.")

        # tarfile 모듈을 사용하여 gzip 압축 방식으로 tar 아카이브 생성
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(folder_path, arcname=folder_id)

        return True
    except Exception as e:
        print(e.args[0])
        return False
    
def make_asodesign_link(folder_id, html_name="ASO Design files(gzip)",
        host="/", api="ftp/design/result/gz/", cache_path='design_folder/'):
    try:
        #base_dir = os.path.abspath(os.path.join("./../../modules/third_party/asodesign_cache/"))
        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"./../../{cache_path}")
        output_path = os.path.join(base_dir, f"{folder_id}.tar.gz")
        if not os.path.exists(output_path):
            raise Exception(f"The file({output_path}) does not created.")
        # make link
        asodesign_link = f"<a href='{host}{api}{folder_id}.tar.gz'>{html_name}</a>"
        return asodesign_link
    except Exception as e:
        print(e.args)
        return False