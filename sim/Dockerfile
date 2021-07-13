FROM jyurkiw/pyzel:release-0.0.3

COPY scripts/run_sims /usr/local/bin/run_sims

RUN git clone --depth=1 https://github.com/jyurkiw/py_ecs.git /app/ecs; \
    git clone --depth=1 https://github.com/jyurkiw/ecs-dnd-Monte-Carlo-Simulation.git /app/mcSim; \
    git clone --depth=1 https://github.com/jyurkiw/py_simrunner /app/simrunner; \
    dos2unix /usr/local/bin/run_sims; \
    chmod +x /usr/local/bin/run_sims

CMD run_sims