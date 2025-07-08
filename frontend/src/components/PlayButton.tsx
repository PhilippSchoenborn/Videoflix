import React from 'react';
import styles from './VideoDetailModal.module.css';

type PlayButtonProps = {
  onClick: () => void;
  resolution: string;
};

const PlayButton: React.FC<PlayButtonProps> = ({ onClick, resolution }) => (
  <button
    className={styles.mainPlayButton}
    onClick={onClick}
    title={`Video in ${resolution} abspielen`}
  >
    ▶
  </button>
);

export default PlayButton;
