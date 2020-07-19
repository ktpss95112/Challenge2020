import itertools as it
import sys
import main

def test(argv):
    AI_score = {}
    for AI in argv[1:]:
        AI_score[AI] = {"score": 0, "times": 0}

    AI_list = list(it.combinations(argv[1:], 4))
    for AIs in AI_list:
        AIs_permute = list(it.permutations(AIs,4))
        for AI in AIs_permute:
            AI = ["0"] + list(AI)
            score = main.main(AI)
            for player, score in zip(AI[1:], score):
                AI_score[player]["score"] += score
                AI_score[player]["times"] += 1
    
    for player, result in AI_score.items():
        print(f"{player}\'s score is {result['score'] / result['times']}")


if __name__ == "__main__":
	test(sys.argv)