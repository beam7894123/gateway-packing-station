import React from 'react'
import PropTypes from 'prop-types'
import { CImage } from '@coreui/react'

const FALLBACK_IMAGE_SRC = '../images/404.png'

const ItemImage = ({ src, alt, width, height, style, className }) => {
  const handleImageError = (event) => {
    if (event.target.src !== FALLBACK_IMAGE_SRC) {
      // console.warn(
      //   `Image failed to load: ${event.target.currentSrc || event.target.src}. Falling back to ${FALLBACK_IMAGE_SRC}`,
      // )
      event.target.src = FALLBACK_IMAGE_SRC
    } else {
      console.error('Fallback image failed to load:', FALLBACK_IMAGE_SRC)
    }
  }

  const initialSrc = src || FALLBACK_IMAGE_SRC

  return (
    <CImage
      src={initialSrc}
      alt={alt} // Alt text is passed directly
      width={width}
      height={height}
      style={{ objectFit: 'cover', display: 'block', ...style }}
      className={className}
      onError={handleImageError}
      loading="lazy"
    />
  )
}

// Define PropTypes for type checking and documentation
ItemImage.propTypes = {
  src: PropTypes.string,
  alt: PropTypes.string.isRequired,
  width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  style: PropTypes.object,
  className: PropTypes.string,
}

// Define default props
ItemImage.defaultProps = {
  src: null,
  width: 100,
  height: 100,
  style: {},
  className: '',
}

export default ItemImage
