#TODO Investigate use of GHMM instead
# Viterbi algo implemtantion from wikipedia.
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
     # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    for line in dptable(V):
        print line
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t][previous]["prev"]
 
    print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
 
def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


states = ('Walking', 'Grazing', 'Resting')

# TODO use backward-forward algo to determine proper P values.
observations = ('HighAccel_HighHeading', 'LowAccel_HighHeading', 'HighAccel_LowHeading', 'LowAccel_LowHeading')
start_probability = {'Resting': 0.6, 'Grazing': 0.3, "Walking":0.1}
transition_probability = {
   'Walking' : {'Walking': 0.6, 'Grazing': 0.3, 'Resting': 0.2},
   'Grazing' : {'Grazing': 0.4, 'Resting': 0.4, 'Walking': 0.2},
   'Resting' : {'Resting': 0.7, 'Walking': 0.1, 'Resting': 0.2}
   }
emission_probability = {
   'Walking' : {'HighAccel_HighHeading': 0.1, 'LowAccel_HighHeading': 0.2, 'HighAccel_LowHeading': 0.7, 'LowAccel_LowHeading':0.1},
   'Grazing' : {'HighAccel_HighHeading': 0.1, 'LowAccel_HighHeading': 0.5, 'HighAccel_LowHeading': 0.1, 'LowAccel_LowHeading':0.3},
   'Resting' : {'HighAccel_HighHeading': 0.0, 'LowAccel_HighHeading': 0.2, 'HighAccel_LowHeading': 0.0, 'LowAccel_LowHeading':0.8},

   }

viterbi(observations,
       states,
       start_probability,
       transition_probability,
       emission_probability)

