/* eslint-disable react/destructuring-assignment */
import React from 'react';
import Slider, { Range } from 'rc-slider';
import 'rc-slider/assets/index.css';

const sliderHandle = ({ value, dragging, index, offset, ...restProps }) => {
  const positionStyle = {
    position: 'absolute',
    left: `${offset}%`,
  };
  return (
    <span key={index}>
      <div className="rc-slider-tooltip" style={positionStyle}>
        {`${value}`}
      </div>
      <Slider.Handle value={value} offset={offset} {...restProps} />
    </span>
  );
};

const decimalSliderHandle = ({ value, dragging, index, offset, ...restProps }) => {
  const positionStyle = {
    position: 'absolute',
    left: `${offset}%`,
  };
  return (
    <span key={index}>
      <div className="rc-slider-tooltip" style={positionStyle}>
        {`${Number.parseFloat(value*0.01).toFixed(2)}`}
      </div>
      <Slider.Handle value={value} offset={offset} {...restProps} />
    </span>
  );
};

const SliderTooltip = (props) => {
  return <Slider handle={props.handle || sliderHandle} {...props} />;
};

const RangeTooltip = (props) => {
  return <Range handle={props.handle || sliderHandle} {...props} />;
};

const DecimalSliderTooltip = (props) => {
  return <Slider handle={props.handle || decimalSliderHandle} {...props} />;
};

const DecimalRangeTooltip = (props) => {
  return <Range handle={props.handle || decimalSliderHandle} {...props} />;
};

export { SliderTooltip, RangeTooltip, DecimalSliderTooltip, DecimalRangeTooltip };
