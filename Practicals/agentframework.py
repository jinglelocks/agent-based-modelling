# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:45:52 2022

@author: alexa
"""

import random
import csv
import requests
import bs4

#random.seed = 5

"""
# to get the below create_env function working, I first tested it in this format outside of agentframework:
def csv_func_test(input_file):
    file1 = input_file
    dataset = file1 
    list1 = []
    for row in dataset:
        rowlist=[]
        #print("new row")
        #print(row)
        for values in row:
            rowlist.append(values)
            #print(values) # test how values are read in
        #print(rowlist) # test how the row list looks
        list1.append(rowlist)
    return list1

input_file = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
environment = csv_func_test(input_file)
print(environment)
"""

def create_env(environment_file):
    #pass
    file1 = open(environment_file, newline="")
    dataset = csv.reader(file1, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    # creating the environment by appending input file values to a 2D list
    environment = []
    for row in dataset:
        rowlist=[]
        #print("new row")
        #print(row)
        for values in row:
            rowlist.append(values)
            #print(values) # test how values are read in
        #print(rowlist) # test how the row list looks
        environment.append(rowlist)
    file1.close()
    #print(environment[0:2]) # print a small slice of the environment list
    return environment

class Agent():
# Special methods like the __init__ constructor and other class properties go here
    def __init__ (self, environment, name, agents, y=None, x=None): # self is a variable representing the object is injected into the call, traditionally called self (not a keyword)
        #pass
        if (y == None):
            self._y = random.randint(0,299)
        else:
            self._y = y #random.randint(0,299)
        if (x == None):
            self._y = random.randint(0,299)
        else:
            self._x = x #random.randint(0,299)
        self.environment = environment
        self.store = 0
        self.name = name
        self.agents = agents
        
    # practising making a function inside the class        
    #def randomise(self):
        #self.y = random.randint(0,99)
        #self.x = random.randint(0,99)
    #def hi(self):
        #print("hello world")
    
    def check_other_agent(self):
        """
        function to check if the agents list is being passed into the agent class

        Returns
        -------
        None.

        """
        other_agent = self.agents[4]._x
        print(other_agent)  
    
    def __str__(self):
        """
        str method, overriding the default __str__ by returning the name variable which has been passed into the __init__ constructor above

        Returns
        -------
        String
            Name of agent

        """
        return str(self.name)
        
    def agent_status(self):
        """
        Returns the name, coordinates and store value of an agent

        Returns
        -------
        String
            name
            x
            y
            store

        """
        return str(self.name) + ", x=" + str(self._x) + ", y=" + str(self._y) + ", store=" + str(self.store)

# protecting the y and x variables behind get/set methods
    def get_y(self):
        """
        user-defined methods such as the agent's actions etc follow.
        the below function moves the agent randomly when called
        could use .y here also to call get/set methods defined above
        but since this is inside the agentframework module it's clearer
        to use the private variable _y     

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self._y
        
    def set_y(self, value):
        self._y = value
        
    def del_y(self):
        del self._y
# any code that retrieves the value of y will call get_y()
# any that assigns a value to y will call set_y()
    y = property(get_y, set_y, del_y, "y property")
        
    def get_x(self):
        return self._x
        
    def set_x(self, value):
        self._x = value
        
    def del_x(self):
        del self._x
    
    x = property(get_x, set_x, del_x, "x property")

    def move(self):
        if random.random() < 0.5:
            self._y = (self._y + 1) % 300
        else:
            self._y = (self._y - 1) % 300
        if random.random() < 0.5:
            self._x = (self._x + 1) % 300        
        else:
            self._x = (self._x - 1) % 300 
            
    def eat(self):
        #pass
        if self.environment[self._y][self._x] > 10: # if the environment value is greater than 10
            self.environment[self._y][self._x] -= 10 # 10 is removed from the value
            self.store += 10 # 10 is added to the agent's store (Agent eats 10 units of environment)
        elif self.environment[self._y][self._x] > 0 < 10: # if the value is greater than 0 but less than 10
            self.store += self.environment[self._y][self._x] # store that value first, before it is changed by the next line (agent eats the value)
            self.environment[self._y][self._x] -= self.environment[self._y][self._x] # reducing the value to 0 by subtracting it from itself (agent has eaten the remainder)
        if self.store > 200: # if agent's store exceeds 200
            self.environment[self._y][self._x] += self.store # the environment receives the store value at current location
            self.store -= self.store # the agent's store loses the value (Agent was sick!)
    
    def distance_between(self, agent):
        return (((self._y - agent.y)**2) + ((self._x - agent.x)**2))**0.5
    
    def share_with_neighbours(self, neighbourhood):
        #print(neighbourhood)
        for agent in self.agents:
            if agent != self:
                distance = self.distance_between(agent)
                if distance <= neighbourhood:
                    sum = self.store + agent.store
                    resource_share = sum / 2
                    #print(self, "and", agent, "are close enough to share resources, they share", resource_share, "units.")
                    self.store = resource_share
                    agent.store = resource_share

class Predator(Agent): # creating a subclass of Agent to transfer
    def __init__ (self, environment, name, agents, y, x, predators): # self is a variable representing the object is injected into the call, traditionally called self (not a keyword)
        #pass
        self.predators = predators
        super().__init__(environment, name, agents, y, x)
        
        """
        # no need for these, since they have been inherited from the Agent class
        self._y = random.randint(0,299) #None
        self._x = random.randint(0,299) #None
        self.environment = environment
        self.store = 0
        self.name = name
        self.agents = agents
        self.predators = predators
        """
    def hunt_agent(self, neighbourhood):
        for agent in self.agents[:]:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                #print("Growl")
                self.agents.remove(agent)
                print(agent, "has been eaten")
                
        