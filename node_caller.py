import execjs


def get_js_object(filename):
    node = execjs.get('Node')
    with open(filename, 'r') as f:
        code = f.read()
        ctx = node.compile(code)
        return ctx


def get_personality_by_twitter(twitter, ctx):
    return ctx.call('get_PI_from_twitter', twitter)


def get_personality_by_text(text, ctx):
    return ctx.call('get_PI_from_text', text)


if __name__ == '__main__':
    ctx = get_js_object('JS_module.js')
    print get_personality_by_text(open('texts/obama_text.txt', 'r').read(), ctx)