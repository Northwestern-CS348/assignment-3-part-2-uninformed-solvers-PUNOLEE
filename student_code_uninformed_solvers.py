
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition or self.visited[self.currentState] == False:
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition
        if self.currentState.nextChildToVisit == 0:
            self.append_child()

        if self.currentState.nextChildToVisit < len(self.currentState.children):
            if self.visited[self.currentState.children[self.currentState.nextChildToVisit]] == False:
                state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(state.requiredMovable)
                self.currentState = state
                return self.solveOneStep()
        elif self.currentState.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()

    def append_child(self):
        movables = self.gm.getMovables()
        if movables:
            for move in movables:
                parent = self.currentState
                self.gm.makeMove(move)
                GS = GameState(self.gm.getGameState(), parent.depth + 1, move)
                GS.parent = parent
                if GS not in self.visited:
                    parent.children.append(GS)
                    self.visited[GS] = False
                elif self.visited[GS] == False:
                    parent.children.append(GS)
                self.gm.reverseMove(move)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return self.currentState.state == self.victoryCondition
        cur_depth = self.currentState.depth
        self.visited[self.currentState] = True
        while True:
            if self.traverse_child(cur_depth):
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    cur_depth += 1
            else:
                return False

    def append_child(self):
        movables = self.gm.getMovables()
        if movables:
            for move in movables:
                parent = self.currentState
                self.gm.makeMove(move)
                GS = GameState(self.gm.getGameState(), parent.depth + 1, move)
                GS.parent = parent
                if GS not in self.visited:
                    parent.children.append(GS)
                    self.visited[GS] = False
                elif self.visited[GS] == False:
                    parent.children.append(GS)
                self.gm.reverseMove(move)

    def traverse_child(self, cur_depth):
        if self.currentState.depth == cur_depth:
            if not self.currentState.children and self.visited[self.currentState] == False or cur_depth == 0:
                self.append_child()
            if self.currentState.state == self.victoryCondition or self.visited[self.currentState] == False:
                self.visited[self.currentState] = True
                return self.currentState.state == self.victoryCondition
            else:
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.traverse_child(cur_depth)
        elif self.currentState.depth < cur_depth:
            if self.currentState.nextChildToVisit > len(self.currentState.children):
                self.currentState.nextChildToVisit = 0
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(state.requiredMovable)
                self.currentState = state
                return self.traverse_child(cur_depth)
            else:
                self.currentState.nextChildToVisit += 1
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.traverse_child(cur_depth)
        return False
