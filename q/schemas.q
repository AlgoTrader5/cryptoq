refdata:([]
	sym:`symbol$();
	exch:`symbol$();
	minTick:`float$();
	minSize:`float$();
	makerFee:`float$();
	takerFee:`float$());

fixlog:([]
	utc_datetime:`timestamp$();
	msg_type:`symbol$();
	msg:`symbol$());


trades:([]
	utc_datetime:`timestamp$();
	exch_datetime:`timestamp$();
	exch:`symbol$();
	sym:`symbol$();
	side:`symbol$();
	amount:`float$();
	price:`float$();
	tradeid:`symbol$());

