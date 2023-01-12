import Header from '../components/Header';
import LaptopGrid from '../components/LaptopGrid';

function Home({laptops, setLaptopFeatures, setShowLaptopFeatures}) {
	return (
		<div>
			<Header />
			<LaptopGrid
				laptops={laptops}
				setLaptopFeatures={setLaptopFeatures}
				setShowLaptopFeatures={setShowLaptopFeatures}
			/>
		</div>
	);
}

export default Home;
