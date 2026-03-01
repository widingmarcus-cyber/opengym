You are the Coordinator. Your task is to evaluate whether quorum has been reached and make a commit/abort decision.

1. Read `setup/votes.json` (contains votes from participating nodes).
2. Determine the total number of nodes in the system (there are 3 total: A, B, C).
3. Count how many votes were actually received (not all nodes may have voted).
4. Calculate the quorum threshold: a **strict majority** of total nodes (i.e., more than half).
5. Determine:
   - How many votes were received
   - How many votes are needed for quorum
   - Whether quorum was reached
   - The decision: `"commit"` if quorum is reached and all received votes are `"commit"`, otherwise `"abort"`
6. Write your analysis to `setup/answer.json` with keys:
   - `"quorum_reached"`: boolean
   - `"votes_received"`: number of votes cast
   - `"votes_needed"`: minimum votes required for quorum
   - `"decision"`: `"commit"` or `"abort"`
