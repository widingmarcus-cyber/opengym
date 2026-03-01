#!/usr/bin/env python3
"""Verification script for Challenge 162: Partial Quorum"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: votes.json exists and is valid
    votes_path = os.path.join(SETUP_DIR, "votes.json")
    if not os.path.exists(votes_path):
        print(json.dumps({"test": "votes_exists", "passed": False, "message": "setup/votes.json does not exist"}))
        sys.exit(0)

    try:
        with open(votes_path, "r") as f:
            votes = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "votes_valid", "passed": False, "message": f"Could not parse votes.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "votes_exists", "passed": True, "message": "votes.json exists and is valid JSON"}))

    # Test 2: votes.json has exactly 2 entries (node_a and node_b)
    has_a = "node_a" in votes
    has_b = "node_b" in votes
    vote_count = len([k for k in votes if k.startswith("node_")])

    if has_a and has_b and vote_count == 2:
        print(json.dumps({"test": "votes_count", "passed": True, "message": "votes.json has 2 entries: node_a and node_b"}))
    else:
        print(json.dumps({"test": "votes_count", "passed": False, "message": f"Expected node_a and node_b only. Keys: {list(votes.keys())}"}))

    # Test 3: Both votes are "commit"
    a_vote = votes.get("node_a", {}).get("vote")
    b_vote = votes.get("node_b", {}).get("vote")
    if a_vote == "commit" and b_vote == "commit":
        print(json.dumps({"test": "votes_commit", "passed": True, "message": "Both nodes voted 'commit'"}))
    else:
        print(json.dumps({"test": "votes_commit", "passed": False, "message": f"Expected both votes 'commit'. node_a={a_vote}, node_b={b_vote}"}))

    # Test 4: answer.json exists and is correct
    answer_path = os.path.join(SETUP_DIR, "answer.json")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.json does not exist"}))
        return

    try:
        with open(answer_path, "r") as f:
            answer = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "answer_valid", "passed": False, "message": f"Could not parse answer.json: {e}"}))
        return

    # Check quorum_reached
    if answer.get("quorum_reached") is True:
        print(json.dumps({"test": "answer_quorum", "passed": True, "message": "answer.json quorum_reached is true"}))
    else:
        print(json.dumps({"test": "answer_quorum", "passed": False, "message": f"Expected quorum_reached true, got {answer.get('quorum_reached')}"}))

    # Check votes_received
    if answer.get("votes_received") == 2:
        print(json.dumps({"test": "answer_votes_received", "passed": True, "message": "answer.json votes_received is 2"}))
    else:
        print(json.dumps({"test": "answer_votes_received", "passed": False, "message": f"Expected votes_received 2, got {answer.get('votes_received')}"}))

    # Check votes_needed
    if answer.get("votes_needed") == 2:
        print(json.dumps({"test": "answer_votes_needed", "passed": True, "message": "answer.json votes_needed is 2"}))
    else:
        print(json.dumps({"test": "answer_votes_needed", "passed": False, "message": f"Expected votes_needed 2, got {answer.get('votes_needed')}"}))

    # Check decision
    if answer.get("decision") == "commit":
        print(json.dumps({"test": "answer_decision", "passed": True, "message": "answer.json decision is 'commit'"}))
    else:
        print(json.dumps({"test": "answer_decision", "passed": False, "message": f"Expected decision 'commit', got '{answer.get('decision')}'"}))


if __name__ == "__main__":
    main()
