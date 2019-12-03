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


execs:([]
	utc_datetime:`timestamp$();
	exch_time:`symbol$();
	exch:`symbol$();
	sym:`symbol$();
	side:`symbol$();
	price:`float$();
	exec_qty:`float$();
	trade_id:`symbol$();
	isTaker:`symbol$());

