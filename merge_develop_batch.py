#! python

import sys
import subprocess
import merge_develop

branches = [
        'laj-spikes/delorean/acn-boot',
        'laj-spikes/delorean/acn-lein',
        'laj-spikes/delorean/acn-lein-doo',
        'laj-spikes/proto/es6-nest6',
        'bug/self-service/no-confirm-error',
        'laj/ab-saved-cart-email',
        ]
for branch in branches:
    merge_develop.merge_develop_into(branch)

