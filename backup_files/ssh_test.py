from pexpect import pxssh

def clear_endpoint_post():
    """
    SSH Into leaf and clear EPG entry
    :return:
    """
    print 'starting clear_endpoint_post'
    description = ('WICAT')
    endpoint = '10.44.8.138'
    endpoint_tenant = 'VA2-WU'
    endpoint_vrf = 'WU-SS-vrf'
    endpoint_node_oob = '10.44.193.120'



    s = pxssh.pxssh(timeout=10)
    s.login('10.44.193.120', 'tmagill', 'Password2', auto_prompt_reset=False)
    s.PROMPT = '[\.]+[#$]'

    cmd = 'vsh'
    # results.append('')
    # results.append('# ' + cmd)
    s.sendline(cmd)  # run a command
    s.prompt()  # match the prompt
    print(s.before)
    # results.append(s.before.replace(cmd, ''))

    cmd = 'show system internal epm endpoint ip ' + endpoint
    # results.append('')
    # results.append('# ' + cmd)
    s.sendline(cmd)  # run a command
    s.prompt()  # match the prompt
    print(s.before)
    # results.append(s.before.replace(cmd, ''))

    cmd = 'clear system internal epm endpoint key vrf ' + endpoint_tenant + ':' + endpoint_vrf + ' ip ' + endpoint
    # results.append('')
    # results.append('# ' + cmd)
    s.sendline(cmd)  # run a command
    s.prompt()  # match the prompt
    print(s.before)
    # results.append(s.before.replace(cmd, ''))

    cmd = 'show system internal epm endpoint ip ' + endpoint
    s.sendline(cmd)  # run a command
    s.prompt()  # match the prompt
    print(s.before)
    # results.append(s.before.replace(cmd, ''))
    s.logout()


    # cmd = 'show version'
    # print  'CMD:', cmd
    # s.sendline(cmd)  # run a command
    # cmd = 'show vlan'
    # print  'CMD:', cmd
    # print 'PROMPT:', s.prompt
    # s.sendline(cmd)  # run a command
    # s.prompt()  # match the prompt
    # print(s.before)
    # # results.append(s.before.replace(cmd, ''))
    # s.logout()

if __name__ == '__main__':
    clear_endpoint_post()