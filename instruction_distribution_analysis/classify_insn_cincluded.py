

IARITH = [	"add" ,
	"addi" ,
	"addiw" ,
	"addw" ,
	"sub",
	"subw",
	"div",
	"divu",
	"divuw",
	"divw",
	"rem",
	"remu",
	"remuw",
	"remw",
	"mul",
	"mulh",
	"mulhsu",
	"mulhu",
	"mulw",

	"c.add",
	"c.addi4spn",
	"c.addi",
	"c.addw",

	"c.sub",
	"c.subw",

	"c.mv"
	]

AMO = [
	"amoadd.d",
	"amoadd.w",
	"amoand.d",
	"amoand.w",
	"amomax.d",
	"amomaxu.d",
	"amomaxu.w",
	"amomax.w",
	"amomin.d",
	"amominu.d",
	"amominu.w",
	"amomin.w",
	"amoor.d",
	"amoor.w",
	"amoswap.d",
	"amoswap.w",
	"amoxor.d",
	"amoxor.w"
	]

FARITH = ["fadd.d",
	"fadd.q",
	"fadd.s",
	"fdiv.d",
	"fdiv.q",
	"fdiv.s",
	"fmadd.d",
	"fmadd.q",
	"fmadd.s",
	"fmsub.d",
	"fmsub.q",
	"fmsub.s",
	"fmul.d",
	"fmul.q",
	"fmul.s",
	"fnmadd.d",
	"fnmadd.q",
	"fnmadd.s",
	"fnmsub.d",
	"fnmsub.q",
	"fnmsub.s",
	"fsqrt.d",
	"fsqrt.q",
	"fsqrt.s",
	"fsub.d",
	"fsub.q",
	"fsub.s",
]



FMOV = [
	"fmv.d.x",
	"fmv.w.x",
	"fmv.x.d",
	"fmv.x.w",
]

FMAX_MIN = [
	"fmax.d",
	"fmax.q",
	"fmax.s",
	"fmin.d",
	"fmin.q",
	"fmin.s"
]

FSGN_INJECT = [
	"fsgnj.d",
	"fsgnj.q",
	"fsgnjn.d",
	"fsgnjn.q",
	"fsgnjn.s",
	"fsgnj.s",
	"fsgnjx.d",
	"fsgnjx.q",
	"fsgnjx.s",
]

FMEM = [
	"fld",
	"flq",
	"flw",
	"fsd",
	"fsq",
	"fsw",

	"c.fld",
	"c.fldsp",
	"c.flw",
	"c.flwsp",
	"c.fsd",
	"c.fsdsp",
	"c.fsw",
	"c.fswsp"
]

FCOMPARE = [
	"feq.d",
	"feq.q",
	"feq.s",
	"fle.d",
	"fle.q",
	"fle.s",
	"flt.d",
	"flt.q",
	"flt.s"
]

FCLASS = [
	"fclass.d",
	"fclass.q",
	"fclass.s"
]

FCONV = [
	"fcvt.d.l",
	"fcvt.d.lu",
	"fcvt.d.q",
	"fcvt.d.s",
	"fcvt.d.w",
	"fcvt.d.wu",
	"fcvt.l.d",
	"fcvt.l.q",
	"fcvt.l.s",
	"fcvt.lu.d",
	"fcvt.lu.q",
	"fcvt.lu.s",
	"fcvt.q.d",
	"fcvt.q.l",
	"fcvt.q.lu",
	"fcvt.q.s",
	"fcvt.q.w",
	"fcvt.q.wu",
	"fcvt.s.d",
	"fcvt.s.l",
	"fcvt.s.lu",
	"fcvt.s.q",
	"fcvt.s.w",
	"fcvt.s.wu",
	"fcvt.w.d",
	"fcvt.w.q",
	"fcvt.w.s",
	"fcvt.wu.d",
	"fcvt.wu.q",
	"fcvt.wu.s",
]

IMEM = [
	"lb",
	"lbu",
	"ld",
	"lh",
	"lhu",
	"lr.d",
	"lr.w",
	"lui",
	"lw",
	"lwu",
	"sb",
	"sc.d",
	"sc.w",
	"sd",
	"sh",
	"sw",
	"fence",
	"fence.i",

	"c.li",
	"c.lui",
	"c.lw",
	"c.lwsp",
	"c.sw",
	"c.swsp"
]

ILOGIC = [
	"and",
	"andi",
	"or",
	"ori",
	"sll",
	"slli",
	"slliw",
	"sllw",
	"slt",
	"slti",
	"sltiu",
	"sltu",
	"sra",
	"srai",
	"sraiw",
	"sraw",
	"sret",
	"srl",
	"srli",
	"srliw",
	"srlw",
	"xor",
	"xori",

	"c.and",
	"c.andi",
	"c.or",
	"c.slli",
	"c.srai",
	"c.srli",
	"c.xor"
]


REG = [
	"csrrc",
	"csrrci",
	"csrrs",
	"csrrsi",
	"csrrw",
	"csrrwi",
]

COMP_BRANCHES_SYSCALLS = [
	"auipc",
	"beq",
	"bge",
	"bgeu",
	"blt",
	"bltu",
	"bne",
	"ebreak",
	"ecall",
	"dret",
	"jal",
	"jalr",
	"mret",
	"wfi",
	"sfence.vma",

	"c.beqz",
	"c.bnez",
	"c.ebreak",

	"c.jal",
	"c.jalr",
	"c.j",
	"c.jr",
]


# the rest is others




