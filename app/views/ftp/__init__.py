import os
from flask import Blueprint, send_file

bp = Blueprint('ftp', __name__, url_prefix='/ftp')

@bp.route('/design/result/gz/<fileid>.tar.gz')
def asodesign_mergefile(fileid):
    current_path = os.path.dirname(os.path.realpath(__file__))
    #print(fileid)
    asodesign_file = os.path.join(current_path, f"./../../../design_folder/{fileid}.tar.gz")
    return send_file(asodesign_file,
                     mimetype='application/gz',
                     download_name=f'{fileid}.tar.gz',# 다운받아지는 파일 이름. 
                     as_attachment=True)