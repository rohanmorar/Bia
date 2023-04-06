import React from 'react';
import './App.css';

const Bia: React.FC = () => {
  const [show, setShow] = React.useState(false);
  const [expanded, setExpanded] = React.useState(false);
  const [text, setText] = React.useState(['B', 'I', 'A']);

  React.useEffect(() => {
    setTimeout(() => {
      setText(['B', 'e', ' ', 'I', 'A']);
      setTimeout(() => {
        setText(['B', 'e', ' ', 'I', 'm', 'p', 'r', 'o', 'v', 'i', 'n', 'g', ' ', 'A']);
        setTimeout(() => {
          setText(['B', 'e', ' ', 'I', 'm', 'p', 'r', 'o', 'v', 'i', 'n', 'g', ' ', 'A', 'l', 'w', 'a', 'y', 's']);
          setTimeout(() => {
            setExpanded(true);
            setTimeout(() => {
              setText(['B', 'I', 'A']);
              setExpanded(false);
            }, 3000);
          }, 500);
        }, 500);
      }, 500);
    }, 1000);
  }, []);


  return (
    <div className={`BIA ${show ? 'show' : ''}`} style={{ fontSize: '5rem' }}>
      {text.map((char, index) => (
        <span key={index} className={expanded ? 'expanded' : ''}>
          {char}
        </span>
      ))}
    </div>
  );
};

export default Bia;