import Home from "./views/HomeView"
import LaptopFeaturesView from "./views/LaptopFeaturesView"
import { useEffect, useState } from 'react';


function App() {
  const [laptops, setlaptops] = useState({});
  const [laptopFeatures, setLaptopFeatures] = useState();
  const [showLaptopFeatures, setShowLaptopFeatures] = useState(false);

  useEffect(() => {
    fetch(process.env.REACT_APP_API_URL + '/laptop')
      .then((response) => response.json())
      .then((data) => setlaptops(data));
  }, []);

  return (
    <>
      {showLaptopFeatures
        ? <LaptopFeaturesView laptopFeatures={laptopFeatures} setLaptopFeatures={setLaptopFeatures} setShowLaptopFeatures={setShowLaptopFeatures} />
        : <Home laptops={laptops} setLaptopFeatures={setLaptopFeatures} setShowLaptopFeatures={setShowLaptopFeatures} />}

    </>
  );
}

export default App;
