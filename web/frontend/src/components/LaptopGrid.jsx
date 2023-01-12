import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

function LaptopGrid({laptops, setLaptopFeatures, setShowLaptopFeatures}) {
	let clearData = [];
	let chunkedData = [];
	for (const marka in laptops) {
		for (const model in laptops[marka]) {
			const laptopData = {
				marka,
				model,
				amount: laptops[marka][model].amount,
				from: laptops[marka][model].from,
				ozellikler: laptops[marka][model].ozellikler,
			};
			clearData.push(laptopData);
		}
	}
	for (let i = 0; i < clearData.length; i++) {
		let data = clearData[i];
		let foundn11 = false;
		for (let j = 0; j < data.from.length; j++) {
			if (data.from[j].website == 'n11') {
				foundn11 = true;
			}
		}
		if (!foundn11) {
			clearData.splice(i, 1);
			i--;
		}
	}
	chunkedData = clearData.reduce((resultArray, item, index) => {
		const chunkIndex = Math.floor(index / 3);

		if (!resultArray[chunkIndex]) {
			resultArray[chunkIndex] = [];
		}

		resultArray[chunkIndex].push(item);

		return resultArray;
	}, []);
	return (
		<main className='h-screen'>
			<Container fluid>
				{chunkedData.map((row, rowIndex) => (
					<Row key={rowIndex}>
						{row.map((laptop, colIndex) => {
							if ((laptop?.marka + ' ' + laptop?.model).includes('bu modele özgü')) return <></>;
							if ((laptop?.marka + ' ' + laptop?.model).length < 3) return <></>;

							let enUcuzSite = laptop?.from[0];
							let enUcuzSiteIndex;
							let oburSiteler = laptop.from;

							laptop?.from.forEach((item, index) => {
								if (item.fiyat < enUcuzSite.fiyat) {
									enUcuzSite = item;
									enUcuzSiteIndex = index;
								}
							});
							oburSiteler.splice(enUcuzSiteIndex, 1);
							return (
								<Col key={colIndex}>
									<Card
										style={{
											width: '23rem',
										}}>
										<Card.Img
											variant='top'
											style={{
												width: '10rem',
												height: '10rem',
												marginRight: 'auto',
												marginLeft: 'auto',
											}}
											src={laptop?.from[0]?.fotolink}
										/>
										<Card.Body>
											<Card.Title>{laptop?.marka + ' ' + laptop?.model}</Card.Title>
											<Card.Text>
												En ucuz ürün{' '}
												<Card.Link href={enUcuzSite?.link}>
													{enUcuzSite?.website}
												</Card.Link>{' '}
												sitesinde bulunuyor. <br />
												<span
													style={{
														color: 'red',
														fontSize: '1.2rem',
													}}>
													Fiyatı : {enUcuzSite?.fiyat} TL
												</span>
											</Card.Text>
										</Card.Body>
										<ListGroup className='list-group-flush'>
											<ListGroup.Item>
												<Card.Link
													href='#'
													onClick={() => {
														setLaptopFeatures({laptop, enUcuzSite});
														setShowLaptopFeatures(true);
													}}
													style={{
														fontSize: '0.8rem',
													}}>
													Özellikleri detaylı görmek için tıklayın...
												</Card.Link>
											</ListGroup.Item>
										</ListGroup>
										<Card.Body
											style={{
												width: '100%',
												display: 'flex',
												justifyItems: 'space-between',
											}}>
											<ListGroup style={{minHeight: '150px'}} className='list-group-flush'>
												{oburSiteler.map((site) => (
													<ListGroup.Item>
														<Card.Text href='#'>
															<Card.Link href={site?.link}>
																{site?.website}
															</Card.Link>{' '}
															sitesindeki fiyat
															<span
																style={{
																	color: 'red',
																	fontSize: '1.1rem',
																}}>
																{site?.fiyat} TL
															</span>
														</Card.Text>
													</ListGroup.Item>
												))}
											</ListGroup>
										</Card.Body>
									</Card>
								</Col>
							);
						})}
					</Row>
				))}
			</Container>
		</main>
	);
}

export default LaptopGrid;
