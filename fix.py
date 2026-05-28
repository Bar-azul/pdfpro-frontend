content = open('index.html', encoding='utf-8').read()

tag = '<meta name="google-site-verification" content="k8S3mn2vvZS9HIfyJ6pAamCOArNZoVwovXcb573A2Kk"/>'

if tag in content:
    print('Tag already exists!')
else:
    fixed = content.replace(
        '<meta charset="UTF-8"/>',
        '<meta charset="UTF-8"/>\n' + tag
    )
    open('index.html', 'w', encoding='utf-8').write(fixed)
    print('Done! Tag added.')
