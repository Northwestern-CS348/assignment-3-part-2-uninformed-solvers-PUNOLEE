from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        def findDigit(s):
            for ind, c in enumerate(s):
                if c.isdigit():
                    return int(c)
        atuple = [[],[],[]]
        listOfBindings_on = self.kb.kb_ask(parse_input('fact: (on ?d ?p)'))
        if listOfBindings_on:
            for bindings in listOfBindings_on:
                b_d = bindings.bindings_dict['?d']
                b_p = bindings.bindings_dict['?p']
                if b_p == 'peg1':
                    atuple[0].append(findDigit(b_d))
                if b_p == 'peg2':
                    atuple[1].append(findDigit(b_d))
                elif b_p == 'peg3':
                    atuple[2].append(findDigit(b_d))

        state = []
        for t in atuple:
            t.sort()
            state.append(tuple(t))
        return tuple(state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        sl = movable_statement.terms
        # movable disk1 peg2 peg1
        to_retract = list()
        to_assert = list()

        #print(self.kb)
        # retract(fact: (on sl[0] sl[1]))
        to_retract.append(parse_input('fact: (on ' + str(sl[0]) + ' ' + str(sl[1]) + ')'))
        # retract(fact: (top sl[0] sl[1]))
        to_retract.append(parse_input('fact: (top ' + str(sl[0]) + ' ' + str(sl[1]) + ')'))

        # ask(fact: (pred sl[0] ?d)) -> disk retract & assert(fact: (top disk sl[1]))
        answer0 = self.kb.kb_ask(parse_input('fact: (pred ' + str(sl[0]) + ' ?d'))
        if answer0:
            to_retract.append(parse_input('fact: (pred ' + str(sl[0]) + ' ' + answer0[0].bindings_dict['?d'] + ')'))
            to_assert.append(parse_input('fact: (top ' + answer0[0].bindings_dict['?d'] + ' ' + str(sl[1]) + ')'))
        # -> nah -> assert(fact: (empty sl[1]))
        else:
            to_assert.append(parse_input('fact: (empty ' + str(sl[1]) + ')'))

        # assert(fact: (on sl[0] sl[2]))
        to_assert.append(parse_input('fact: (on ' + str(sl[0]) + ' ' + str(sl[2]) + ')'))
        # assert(fact: (top sl[0] sl[2]))
        to_assert.append(parse_input('fact: (top ' + str(sl[0]) + ' ' + str(sl[2]) + ')'))
        # ask(fact: (top ?d sl[2])) -> disk retract & assert(fact: (pred sl[0] disk))

        answer1 = self.kb.kb_ask(parse_input('fact: (top ?d ' + str(sl[2]) + ')'))
        # fact: (empty sl[2]) == True -> retract
        if not answer1:
            to_retract.append(parse_input('fact: (empty ' + str(sl[2]) + ')'))
        else:

            if answer1[0].bindings_dict['?d'] != str(sl[0]):
                to_retract.append(parse_input('fact: (top ' + answer1[0].bindings_dict['?d'] + ' ' + str(sl[2]) + ')'))
                to_assert.append(parse_input('fact: (pred ' + str(sl[0]) + ' ' + answer1[0].bindings_dict['?d'] + ')'))

        for ret in to_retract:
            self.kb.kb_retract(ret)
        for ass in to_assert:
            self.kb.kb_assert(ass)





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        def findDigit(s):
            for ind, c in enumerate(s):
                if c.isdigit():
                    return int(c)
        atuple = [[0,0,0],[0,0,0],[0,0,0]]
        listOfBindings_on = self.kb.kb_ask(parse_input('fact: (on ?t ?x ?y)'))
        if listOfBindings_on:
            for bindings in listOfBindings_on:
                b_t = bindings.bindings_dict['?t']
                b_x = bindings.bindings_dict['?x']
                b_y = bindings.bindings_dict['?y']
                if b_y == 'pos1':
                    atuple[0][findDigit(b_x) - 1] = findDigit(b_t)
                if b_y == 'pos2':
                    atuple[1][findDigit(b_x) - 1] = findDigit(b_t)
                elif b_y == 'pos3':
                    atuple[2][findDigit(b_x) - 1] = findDigit(b_t)

        answer = self.kb.kb_ask(parse_input('fact: (empty ?x ?y)'))
        if answer:
            e_x = answer[0].bindings_dict['?x']
            e_y = answer[0].bindings_dict['?y']
            atuple[findDigit(e_y)-1][findDigit(e_x)-1] = -1

        state = []
        for t in atuple:
            state.append(tuple(t))
        return tuple(state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if not self.isMovableLegal(movable_statement):
            pass
        else:
            sl = movable_statement.terms
            # (movable ?t ?x ?y ?z ?w)
            self.kb.kb_retract(parse_input('fact: (on ' + str(sl[0]) + ' ' + str(sl[1]) + ' ' + str(sl[2]) + ')'))
            self.kb.kb_retract(parse_input('fact: (empty ' + str(sl[3]) + ' ' + str(sl[4]) + ')'))
            self.kb.kb_assert(parse_input('fact: (on ' + str(sl[0]) + ' ' + str(sl[3]) + ' ' + str(sl[4]) + ')'))
            self.kb.kb_assert(parse_input('fact: (empty ' + str(sl[1]) + ' ' + str(sl[2]) + ')'))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
