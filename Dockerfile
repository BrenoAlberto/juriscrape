FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install gnupg wget curl git sudo -y 

# Set up user
ARG USER_ID
ARG GROUP_ID
ARG USER_NAME
RUN groupadd -o -r --gid ${GROUP_ID} ${USER_NAME} \
  && adduser --uid $USER_ID --ingroup ${USER_NAME} --disabled-password --gecos "" ${USER_NAME} \
  && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
  && sudo -lU ${USER_NAME} \
  && sudo usermod -aG sudo ${USER_NAME}

ENV RUNNING_IN_DOCKER true

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs

# Install Google Chrome
RUN  wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends

# Install Oh My Zsh
USER ${USER_NAME}
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.0/zsh-in-docker.sh)" -- \
  -t https://github.com/denysdovhan/spaceship-prompt \
  -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
  -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
  -p git \
  -p ssh-agent \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions

USER root
RUN apt-get --fix-broken install -y \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER ${USER_NAME}
ENV JURISCRAPE_PATH /home/${USER_NAME}/juriscrape

WORKDIR ${JURISCRAPE_PATH}

COPY ./scripts ./scripts
RUN echo "alias install_packages='bash ${JURISCRAPE_PATH}/scripts/install_packages.sh'" >> ~/.zshrc

CMD ["/bin/zsh"]