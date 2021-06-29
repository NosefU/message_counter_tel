from typing import Optional, Union


def get_messages(raw_data: dict, chat_id: Union[int, str], default: Optional[dict]=None) -> Optional[dict]:
    """
    Выковыривает список сообщений из бэкапа сообщений телеги
    :param raw_data: десериализованный json бэкапа сообщений
    :param chat_id: chat_id или название чата
    :param default: значение, которое вернётся в случае отстутствия искомого чата в raw_data
    :return: список словарей-сообщений
    """
    # field_name = 'id' if type(chat_id) == int else 'name'
    # for chat in raw_data['chats']['list']:
    #     if chat[field_name] == chat_id:
    #         return chat['messages']
    # return default
    # field_name = 'id' if type(chat_id) == int else 'name'
    # for chat in raw_data['chats']['list']:
    #     if chat[field_name] == chat_id:
    return raw_data['messages']
    # return default
