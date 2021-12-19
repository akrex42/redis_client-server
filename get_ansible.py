import yaml
import ansible
import os


def prepare_yaml(content):

    content1 = {}
    content2 = {}
    content3 = {}
    content4 = {}
    # content5 = {}

    program_name_1 = content["server"]["install_packages"][0]
    program_name_2 = content["server"]["install_packages"][1]
    file_name_1 = content["server"]["exploit_files"][0]
    file_name_2 = content["server"]["exploit_files"][1]
    args_for_consumer = content["bad_guys"]

    content1.update({"name": "Downloading needed software"})
    content1.update({"community.general.homebrew": {"name": [program_name_1, program_name_2],
                                                    "state": "present"}})
    content2.update({"name": "Copying" + file_name_1})
    content2.update({"ansible.builtin.copy": {"src": "src/" + file_name_1,
                                              "dest": "src/" + file_name_1}})
    content3.update({"name": "Copying" + file_name_2})
    content3.update({"ansible.builtin.copy": {"src": "src/" + file_name_2,
                                              "dest": "src/" + file_name_2}})
    content4.update({"name": "Executing the command"})
    content4.update({"ansible.builtin.command": {"cmd": "/Users/akrex/.brew/bin/python3 src/consumer.py -e "
                                                        + args_for_consumer[0] + "," + args_for_consumer[1]}})
    # content5.update({"ansible.builtin.command": {"cmd": "/Users/akrex/.brew/bin/python3 src/exploit.py"}})

    final_content = {"name": "Creating a new playbook"}
    final_content.update({"hosts": "127.0.0.1"})
    final_content.update({"tasks": [content1, content2, content3, content4]})

    list_content = [final_content]

    return list_content


def write_to_new_file(content_new):

    with open("../todo.yml", "w+") as new_script:
        new_script.write(content_new)
        new_script.seek(0)
        os.rename("../todo.yml", "../deploy.yml")


def yaml_load():

    with open("../todo.yml", "r+") as old_script:
        content = yaml.load(old_script.read(), yaml.Loader)
        old_script.seek(0)

    return content


def yaml_dump(list_content):

    content_new = yaml.dump(list_content, sort_keys=False)

    return content_new


if __name__ == "__main__":

    content = yaml_load()
    list_content = prepare_yaml(content)
    content_dumped = yaml_dump(list_content)
    write_to_new_file(content_dumped)
