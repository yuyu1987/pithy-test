#!/usr/bin/python
# coding=utf-8
import os
from click import echo, style
from .utils import mkdir_project, get_project_path, get_templates, cd, render_template, jinja_env


def generate_project(project_name, project_type):
    """
    生成项目
    :param project_name: 项目名称
    :param project_type: 项目类型
    """
    echo(style(u'开始创建%s项目' % project_name, fg='red'))

    # 创建项目文件夹
    mkdir_project(project_name)
    project_path = get_project_path(project_name)

    # 获取所有模版文件
    templates = get_templates(project_type)

    with cd(project_path):
        echo(style(u'开始渲染...', fg='green'))
        for template in templates:
            target_file_name = os.path.splitext(template)[0]
            target_full_name = os.path.join(project_path, target_file_name[len(project_type) + 1:])
            try:
                render_template(jinja_env, template, target_full_name, project_name=project_name)
                echo(style(u'生成 %-32s ' % target_file_name, fg='green') +
                     style(u'[√]', fg='blue'))
            except Exception as e:
                echo(style(u'生成 %-32s ' % target_file_name, fg='red') +
                     style(u'[×]\n', fg='blue'))
                raise Exception
    echo(style(u'生成成功,请使用编辑器打开该项目', fg='red'))


if __name__ == '__main__':
    generate_project('abc', 'interface')