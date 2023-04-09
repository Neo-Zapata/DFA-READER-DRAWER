import numpy as np
import pandas as pd
import graphviz
import os

dot = graphviz.Digraph()

cwd = os.getcwd()
data = pd.read_csv(cwd + "/test.csv")

column_names = data.columns
alphabet = column_names[2:] # because we know the first 2 are final and state (the rest is the alphabet)

dfa = {}

start_state = "q0"
final_states = []
transitions = {}


for index, row in data.iterrows(): # it allows any alphabet, as long as it is declared in the first line of the csv
    row = row.tolist()

    subtransitions = {}
    state = "q" + str(row[1])
    dot.node(state)

    # getting finnal states
    if(row[0] == 'F' or row[0] == 'f'):
        final_states.append("q" + str(row[1]))
        dot.node(state, shape='doublecircle')
    
    iter = 2 # because 2 is where the alphabet starts
    for letter in alphabet: # 0 and 1
        destination_state = "q" + str(row[iter])
        subtransitions[letter] = destination_state
        dot.edge(state, destination_state, label=letter)
        iter += 1

    transitions[state] = subtransitions

dfa["start state"] = start_state
dfa["final states"] = final_states
dfa["transition"] = transitions

def simulate_dfa(dfa, string):
    current_state = dfa["start state"]
    for letter in string:
        if letter not in dfa["transition"][current_state]:
            return False
        current_state = dfa["transition"][current_state][letter]
    return (current_state in dfa["final states"])

def main():
    dot.render("automata", view=True)
    string = input("Enter a string to validate: ")
    is_valid = simulate_dfa(dfa, string)
    print(is_valid)

main()