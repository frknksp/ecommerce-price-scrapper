import React from 'react';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

function LaptopFeaturesView({laptopFeatures, setShowLaptopFeatures, setLaptopFeatures}) {
	const {laptop, enUcuzSite} = laptopFeatures;
	console.log(laptop);
	return (
		<div style={{width: '100%', display: 'flex', justifyContent: 'center'}}>
			<Button
				onClick={() => {
					window.location.reload();
					setLaptopFeatures({});
					setShowLaptopFeatures(false);
				}}
				style={{position: 'absolute', top: '10px', left: '10px'}}
				variant='outline-success'>
				Go back
			</Button>{' '}
			<Card
				style={{
					width: '80%',
					height: '100%',
					background: '#efefef',
				}}>
				<Card.Img
					variant='top'
					style={{
						width: '18rem',
						height: '18rem',
						marginRight: 'auto',
						marginLeft: 'auto',
					}}
					src={laptop?.from[0]?.fotolink}
				/>
				<Card.Body style={{width: '100%', display: 'flex', justifyContent: 'center'}}>
					<Card.Title>{laptop?.marka + ' ' + laptop?.model} Özellikleri</Card.Title>
				</Card.Body>

				<Card.Body
					style={{
						width: '100%',
						display: 'flex',
						justifyItems: 'space-between',
					}}>
					<ListGroup
						className='list-group-flush'
						style={{width: '100%', padding: '0 20%', margin: '20px 0  '}}>
						{Object.keys(laptop?.ozellikler).map((ozellik) => (
							<ListGroup.Item
								style={{
									display: 'flex',
									justifyContent: 'space-between',
									width: '100%',
								}}>
								<span>{ozellik}</span>
								<span>{laptop?.ozellikler[ozellik]}</span>
							</ListGroup.Item>
						))}
					</ListGroup>
				</Card.Body>
			</Card>
		</div>
	);
}

export default LaptopFeaturesView;
