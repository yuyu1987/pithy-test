#!/usr/bin/python
# coding=utf-8
import os
import sys
import contextlib
from jinja2 import FileSystemLoader, Environment
from click import echo, style

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

jinja_env = (lambda: Environment(loader=FileSystemLoader(template_dir)))()


@contextlib.contextmanager
def cd(d):
    cwd = os.getcwd()
    os.chdir(d)
    yield
    os.chdir(cwd)


def mkdir_project(project_name):
    if os.path.exists(project_name) and os.path.isdir(project_name):
        return
    try:
        os.mkdir(project_name)
    except OSError as e:
        echo(style(u"创建 %s 失败, %s" % (project_name, str(e)), fg='red'))
        sys.exit(1)


def get_project_path(project_name):
    return os.path.join(os.getcwd(), project_name)


def get_templates(project_type):
    templates = []

    def get_file_name(folder, base_dir):
        for name in os.listdir(base_dir):
            full_path = os.path.join(base_dir, name)
            if os.path.isfile(full_path):
                templates.append(os.path.join(project_type, folder, name))
            else:
                get_file_name(name, full_path)

    project_template_dir = os.path.join(template_dir, project_type)
    get_file_name('', project_template_dir)
    templates = [file_name.replace('\\', '/') for file_name in templates]
    return templates


def render_template(jinja_env, template, target_full_name, **kwargs):
    """
    渲染横版
    :param jinja_env: jinja环境对象
    :param template: 模版名称
    :param target_full_name: 目录文件全路径
    :param kwargs: 参数
    :return:
    """

    content = jinja_env.get_template(template).render(**kwargs).encode('utf-8')
    target_dir = os.path.dirname(target_full_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(target_full_name, 'w') as f:
        f.write(content)
