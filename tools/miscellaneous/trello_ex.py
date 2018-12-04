"""Example to integrate with py-trello project.

https://pypi.org/project/py-trello/

Ideas for next steps:
    - turn into CLI tool
    - Find cards that have been moved around more than 10 times
    - Find cards that haven't been touched for a really long time
    - Enable duplication of tickets from a certain list on a schedule
"""
#!/usr/bin/env python
import os

from trello import TrelloClient


def main():
    client = TrelloClient(api_key=os.environ.get('TRELLO_API_KEY'),
                     api_secret=os.environ.get('TRELLO_API_SECRET'),
                    )
    trello_filter = 'open'
    open_boards = client.list_boards(board_filter=trello_filter)
    for board in open_boards:
        print board.name
    planner = [board for board in open_boards if board.name == 'Planner']
    if planner:
        planner = planner[0]
    else:
        raise Exception("Planner board not found")
    lists = planner.list_lists(list_filter=trello_filter)
    for l in lists:
        # l.add_card("name of card", "Comment")
        print l.name
        # card_filter is 'open' by default, everything else is 'all'
        for c in l.list_cards(card_filter=trello_filter):
            print u'- {}'.format(c.name)
            movements = c.list_movements()
            print "Moved {} times".format(len(movements))
            # print c.fetch_comments(force=True)
            print c.card_created_date
            print c.date_last_activity


if __name__ == '__main__':
    main()
