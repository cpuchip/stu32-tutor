# stu32-calc's image (calc/build.sh builds it; never pushed to a registry). The stage holds only
# the stripped runners, Casimir's CLI, the entry program, the pins and the key-name page, under
# /opt/stu32, and the licences at /licenses. The base has no shell and no package manager; the
# entry program does its own limits.
ARG BASE
FROM ${BASE}
COPY opt/stu32 /opt/stu32
COPY licenses /licenses
USER 65532:65532
ENTRYPOINT ["/opt/stu32/bin/stu32-calc"]
