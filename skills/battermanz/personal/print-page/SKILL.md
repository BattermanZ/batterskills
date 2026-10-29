---
name: print-page
description: "Put a PDF on print.battercloud.cc so the user can print it from a shop computer. Use when the user sends a document to print away from home, says \"print page\", or says a document on it is printed."
metadata:
  version: "1.0.0"
---

# Print page

print.battercloud.cc is a password page on batterdock that shows every PDF in one folder there. The user opens it on a shop computer, opens the PDF and prints. The stack is `stackyard/batterdock/print` in the batterlab checkout (`~/coding/batterlab`); the header of its `compose.yml` holds the publish and withdraw commands, and its `secrets.sops.env` holds the password. The documents are personal (the first was an energy bill with a home address), so a file stays on the page only until it is printed, and a sidecar deletes anything older than 24 hours regardless.

The work needs ssh to batterdock and the batterlab checkout, which a Claude Code session on BatterCode has. A session without them tells the user to send the PDF to one that has them.

## Steps

1. **Publish.** Name the file so the user recognises it on the page (`Greenchoice-nota-sept-2026.pdf`, not the upload's hash). Stream it over ssh and place it with `install`, which stamps the copy with the current time:

   ```
   ssh batterdock 'umask 077; cat > /tmp/print-upload.pdf && sudo install -m 0644 /tmp/print-upload.pdf /home/battermanz/docker/print/files/<Name>.pdf && rm /tmp/print-upload.pdf' < <local file>
   ```

   The sweep judges age by modification time, so a copy that keeps the original's time (`cp -p`, `scp -p`, `rsync -t`) is deleted within ten minutes. Only `.pdf` files show on the page. Done when the file is in the folder.

2. **Verify from outside.** From the batterlab root, write the password into a header file and fetch the list and the file through the public name:

   ```
   umask 077; sops -d stackyard/batterdock/print/secrets.sops.env | sed -n 's/^PRINT_PASSWORD=/X-Print-Password: /p' > <scratch>/print-header
   curl -s -H @<scratch>/print-header https://print.battercloud.cc/files/
   curl -s -o /dev/null -w '%{http_code} %{content_type}\n' -H @<scratch>/print-header https://print.battercloud.cc/files/<Name>.pdf
   ```

   Delete the header file afterwards. Each visitor gets 20 requests a minute on `/files/`, so a burst of checks earns a 429 that clears within a minute. Done when the list names the file and the file answers `200 application/pdf`.

3. **Hand over.** Give the user the bare address, https://print.battercloud.cc, and the three moves: enter the password, Open PDF, Ctrl+P. Say when the file deletes itself (24 hours after step 1). The user knows the password, so it stays out of the reply unless they ask for it.

4. **Withdraw** when the user says it is printed: `ssh batterdock 'sudo rm /home/battermanz/docker/print/files/<Name>.pdf'`, then rerun the list check from step 2. Done when the list no longer names the file.

## Changing the page itself

The page, the nginx config and the password are repo files: `_deploy/site/index.html`, `_deploy/templates/print.conf.template`, `secrets.sops.env`. A change goes through batterlab's stack pipeline (its `AGENTS.md`, "Compose stacks"), committed and pushed on `main`, never edited on the host. A new password is re-encrypted with `sops` from the batterlab root, so the path matches its creation rule.
