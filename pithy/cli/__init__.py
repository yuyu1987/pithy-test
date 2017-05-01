#!/usr/bin/python
# coding=utf-8
import click
from .init import generate_project


def _validate_project_name(ctx, argument, value):
    """
    验证输入的项目名称是否正确
    """
    if not value or ' ' in value:
        raise click.BadParameter(u"项目名称中不能含有空格")
    return value


def _validate_project_type(ctx, argument, value):
    """
    验证输入的项目类型是否正确
    """
    if not value in ('app', 'api'):
        raise click.BadParameter(u"项目类型不正确")
    return value


@click.group()
@click.version_option()
def cli():
    """
     pithy-cli是一个接口测试项目生成脚手架,功能完善中
    """


@cli.command()
@click.pass_context
@click.option('--project-type', prompt=click.style(u"请选择项目类型,输入api或者app", fg='green'),
              callback=_validate_project_type, help=u"请选择项目类型,输入api或者app")
@click.option('--project-name', prompt=click.style(u"请输入项目名称,如pithy-api-test", fg='green'),
              callback=_validate_project_name, help=u"请输入项目名称,如pithy-api-test")
def init(ctx, project_type, project_name):
    """
    生成接口测试项目

    使用方法:
        $ pithy-cli init         # 生成接口测试项目
    """
    generate_project(project_name, project_type)
