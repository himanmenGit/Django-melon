from django import template

register = template.Library()


def ellipsis_line(value, arg):
    # value로 부터
    # arg에 주어진 line 수만큼의
    # 문자열(Line)을 반환.
    # 만약 arg의 line 수보다
    #   value의 line이 많으면
    #   마지막에 ...추가
    lines = value.splitlines()
    if len(lines) > arg:
        return '\n'.join(lines[:arg] + ['...'])

    return value


register.filter('ellipsis_line', ellipsis_line)
