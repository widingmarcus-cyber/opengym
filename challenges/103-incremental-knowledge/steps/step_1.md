# Step 1: First Requirement — Port and TLS

You are building a server configuration incrementally. Requirements will arrive one at a time across multiple sessions.

**Requirement 1:** The server must listen on **port 8443** and use **HTTPS with TLS 1.3**.

Create `setup/constraints.json` to track all requirements as they arrive. Write this first requirement there in a structured format so you can read it back in future sessions.

You will receive additional requirements in later sessions. Make sure your storage format can accommodate new entries.
