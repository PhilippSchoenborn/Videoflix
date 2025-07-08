import React from 'react';
import styles from './VideoPlayer.module.css';

interface VideoInfoProps {
  title: string;
  quality: string;
}

const VideoInfo: React.FC<VideoInfoProps> = ({ title, quality }) => (
  <div className={styles.videoInfo}>
    <h3>{title}</h3>
    <p>Quality: {quality}</p>
  </div>
);

export default VideoInfo;
