# app/views/utils/__init__.py
import os
import json
import time
from app.utils.refflat import get_refFlat_name
from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint("utils", __name__, url_prefix="/utils")


@bp.route('/getgene', methods=["GET", "POST"])
def debug():
    if request.method == "POST":
        return "test"
    elif request.method == "GET":
        geneName = request.args.get('genename')
        #print(geneName)
        geneNames_list = get_refFlat_name(geneName=geneName,
                 refFlat_genename_path=None)
        return geneNames_list

