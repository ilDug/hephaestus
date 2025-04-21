export class Node {
    constructor(id: string, x: number, y: number) {
        this.id = id;
        this.x = x;
        this.y = y;
    }

    /* The id of the node */
    id: string;

    /**  coordinata ascissa in mm */
    x: number;

    /** coordinata ordinata in mm */
    y: number;

    /** vincoli (x, y, rz) in coordinate globali (1 = vincolato, 0 = libero) */
    restraints: number[] = [0, 0, 0];

    /** carichi (fx, fy, mz) in coordinate globali (N, N, Nm) */
    loads: number[] = [0, 0, 0];

    /** Vincoli globali del nodo. TRUE = fix; FALSE = free */
    public setRestraints(
        x: number | boolean = false,
        y: number | boolean = false,
        rz: number | boolean = false
    ) {
        this.restraints[0] = x ? 1 : 0;
        this.restraints[1] = y ? 1 : 0;
        this.restraints[2] = rz ? 1 : 0;
    }

    /** applica i carichi al nodo. fx, fy ,mz in coordinate globali in kN e kNm */
    public applyLoads(fx: number = 0, fy: number = 0, mz: number = 0) {
        this.loads[0] = fx * 1000;
        this.loads[1] = fy * 1000;
        this.loads[2] = mz * 1000000;
    }
}
