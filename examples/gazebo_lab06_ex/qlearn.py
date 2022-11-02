import random
import pickle


class QLearn:
    def __init__(self, actions, epsilon, alpha, gamma):
        self.q = {}
        self.epsilon = epsilon  # exploration constant
        self.alpha = alpha      # discount constant
        self.gamma = gamma      # discount factor
        self.actions = actions

    def loadQ(self, filename):
        '''
        Load the Q state-action values from a pickle file.
        '''
        
        # TODO: Implement loading Q values from pickle file.
        with open(filename) as f:
            self.q = pickle.load(f)

        print("Loaded file: {}".format(filename+".pickle"))

    def saveQ(self, filename):
        '''
        Save the Q state-action values in a pickle file.
        '''
        # TODO: Implement saving Q values to pickle and CSV files.
        print(f'Saving: {format.self.q}')
        with open(filename,'wb') as f:
            pickle.dump(self.q,f)


        print("Wrote to file: {}".format(filename+".pickle"))

    def getQ(self, state, action):
        '''
        @brief returns the state, action Q value or 0.0 if the value is 
            missing
        '''
        return self.q.get((state, action), 0.0)

    def chooseAction(self, state, return_q=False):
        '''
        @brief returns a random action epsilon % of the time or the action 
            associated with the largest Q value in (1-epsilon)% of the time
        '''
        # TODO: Implement exploration vs exploitation
        #    if we need to take a random action:
        #       * return a random action
        #    else:
        #       * determine which action has the highest Q value for the state 
        #          we are in.
        #       * address edge cases - what if 2 actions have the same max Q 
        #          value?
        #       * return the action with highest Q value
        #
        # NOTE: if return_q is set to True return (action, q) instead of
        #       just action
        
        # THE NEXT LINE NEEDS TO BE MODIFIED TO MATCH THE REQUIREMENTS ABOVE
        
        # Find current q values
        q = [self.getQ(state,a) for a in self.actions]
        max_q = max(q)
        min_q = min(q)

        # do a random action epislon % of the time
        # (epsilon = 1% means random from [0,1) < epsilon about 1% of the time)
        if random.random() < self.epsilon:
            # choose a random action (left, forward, right)
            a = random.randint(0,2)
        else:
            # check if there is more than one max_q value
            b = q.count(max_q)
            
            # if there is more than one max_q, pick on randomly
            if b > 1:
                choices = [c for c in range(len(self.actions)) if q[c] == max_q]
                a = random.choice(choices)
            else:
                a = q.index(max_q)

        action = self.actions[a]

        # display values
        print(f'State: {state} \n Forward: {self.getQ(state,0)} \n Left: {self.getQ(state,1)} \n' 
        f'Right {self.getQ(state,2)} \n Action: {action}')

        if return_q:
            return action, q
        else:
            return action


    def learn(self, state1, action1, reward, state2):
        '''
        @brief updates the Q(state,value) dictionary using the bellman update
            equation
        '''
        # TODO: Implement the Bellman update function:
        #     Q(s1, a1) += alpha * [reward(s1,a1) + gamma* max(Q(s2)) - Q(s1,a1)]
        # 
        # NOTE: address edge cases: i.e. 
        # 
        # Find Q for current (state1, action1)
        # Address edge cases what do we want to do if the [state, action]
        #       is not in our dictionary?
        # Find max(Q) for state2
        # Update Q for (state1, action1) (use discount factor gamma for future 
        #   rewards)

        max_q = max([self.getQ(state2,a) for a in self.actions])
        current_q = self.q.get((state1,action1), None)

        if current_q is None:
            self.q[(state1,action1)] = reward
        elif reward < current_q + self.alpha * (reward+self.gamma+max_q-current_q):
            self.q[(state1,action1)] = current_q+self.alpha*(reward+self.gamma*max_q-current_q)

