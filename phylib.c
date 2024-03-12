#include "phylib.h"

//still ball constructor
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){

    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(newObj == NULL){
        return NULL;
    }

    newObj->type = PHYLIB_STILL_BALL;

    newObj->obj.still_ball.number = number;
    newObj->obj.still_ball.pos.x = pos->x;
    newObj->obj.still_ball.pos.y = pos->y;

    return newObj;

}

//rolling ball constructor
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){
    
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(newObj == NULL){
        return NULL;
    }

    newObj->type = PHYLIB_ROLLING_BALL;

    newObj->obj.rolling_ball.number = number;

    newObj->obj.rolling_ball.pos.x = pos->x;
    newObj->obj.rolling_ball.pos.y = pos->y;

    newObj->obj.rolling_ball.vel.x = vel->x;
    newObj->obj.rolling_ball.vel.y = vel->y;

    newObj->obj.rolling_ball.acc.x = acc->x;
    newObj->obj.rolling_ball.acc.y = acc->y;

    return newObj;

}

//hole constructor
phylib_object *phylib_new_hole(phylib_coord *pos){
    
    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(newObj == NULL){
        return NULL;
    }

    newObj->type = PHYLIB_HOLE;

    newObj->obj.hole.pos.x = pos->x;
    newObj->obj.hole.pos.y = pos->y;

    return newObj;

}

//hcushion constructor
phylib_object *phylib_new_hcushion(double y){

    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(newObj == NULL){
        return NULL;
    }

    newObj->type = PHYLIB_HCUSHION;

    newObj->obj.hcushion.y = y;

    return newObj;

}

//vcushion constructor
phylib_object *phylib_new_vcushion(double x){

    phylib_object *newObj = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(newObj == NULL){
        return NULL;
    }

    newObj->type = PHYLIB_VCUSHION;

    newObj->obj.vcushion.x = x;

    return newObj;

}

//table constructor
phylib_table *phylib_new_table(){

    phylib_table *table = (phylib_table *)malloc(sizeof(phylib_table));

    //check for failed malloc
    if(table == NULL){
        return NULL;
    }

    //Initialize all values
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        table->object[i] = NULL;
    }

    table->time = 0.0;

    //add hcushions
    phylib_object *hCushion1 = phylib_new_hcushion(0.0);
    phylib_object *hCushion2 = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    table->object[0] = hCushion1;
    table->object[1] = hCushion2;

    //add vcushions
    phylib_object *vCushion1 = phylib_new_vcushion(0.0);
    phylib_object *vCushion2 = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    table->object[2] = vCushion1;
    table->object[3] = vCushion2;

    //add holes
    phylib_coord c;
    c.x = 0.0;
    c.y = 0.0;
    phylib_object *hole1 = phylib_new_hole(&c);
    c.y = PHYLIB_TABLE_LENGTH/2.0;
    phylib_object *hole2 = phylib_new_hole(&c);

    table->object[4] = hole1;
    table->object[5] = hole2;

    c.x = 0.0;
    c.y = PHYLIB_TABLE_LENGTH;
    phylib_object *hole3 = phylib_new_hole(&c);
    c.x = PHYLIB_TABLE_WIDTH;
    c.y = 0.0;
    phylib_object *hole4 = phylib_new_hole(&c);

    table->object[6] = hole3;
    table->object[7] = hole4;

    c.x = PHYLIB_TABLE_WIDTH;
    c.y = PHYLIB_TABLE_LENGTH/2.0;
    phylib_object *hole5 = phylib_new_hole(&c);
    c.y = PHYLIB_TABLE_LENGTH;
    phylib_object *hole6 = phylib_new_hole(&c);

    table->object[8] = hole5;
    table->object[9] = hole6;

    return table;

}

//copy phylib object
void phylib_copy_object(phylib_object **dest, phylib_object **src){

    //check for null object
    if(*src == NULL){
        *dest = NULL;
        return;
    }

    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    //check for failed malloc
    if(*dest == NULL){
        return;
    }

    //copy memory
    memcpy(*dest, *src, sizeof(phylib_object));

}

//copy phylib table
phylib_table *phylib_copy_table(phylib_table *table){

    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    //check for failed malloc
    if(newTable == NULL){
        return NULL;
    }

    //copy time
    newTable->time = table->time;

    //copy all objects using copy object function
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        phylib_copy_object(&newTable->object[i], &table->object[i]);
    }

    return newTable;

}

//add object to table
void phylib_add_object(phylib_table *table, phylib_object *object){

    //find first empty space if there is one
    int i = 0;
    while(i < PHYLIB_MAX_OBJECTS && table->object[i] != NULL){
        i++;
    }

    //If there's an empty space add object
    if(i < PHYLIB_MAX_OBJECTS){
        table->object[i] = object;
    }

}

//free table
void phylib_free_table(phylib_table *table){

    if(table == NULL){
        return;
    }

    //free all objects
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        free(table->object[i]);
    }

    //free table
    free(table);

}

//subtract coordinates
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){

    phylib_coord sub;
    sub.x = c1.x - c2.x;
    sub.y = c1.y-c2.y;
    return sub;

}

//get the length of a coordinate
double phylib_length(phylib_coord c){

    double length = 0;
    length += c.x * c.x;
    length += c.y * c.y;
    length = sqrt(length);

    return length;

}

//get the dot product of two vectors
double phylib_dot_product(phylib_coord a, phylib_coord b){

    double product = a.x * b.x;
    product += a.y * b.y;
    return product;

}

//get the distance between two objects
double phylib_distance(phylib_object *obj1, phylib_object *obj2){

    if(obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }

    double dist = 0;

    if(obj2->type == PHYLIB_ROLLING_BALL){

        phylib_coord line = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        dist = phylib_length(line);
        dist -= PHYLIB_BALL_DIAMETER;

    }else if(obj2->type == PHYLIB_STILL_BALL){

        phylib_coord line = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        dist = phylib_length(line);
        dist -= PHYLIB_BALL_DIAMETER;

    }else if(obj2->type == PHYLIB_HOLE){

        phylib_coord line = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        dist = phylib_length(line);
        dist -= PHYLIB_HOLE_RADIUS;

    }else if(obj2->type == PHYLIB_HCUSHION){
        
        dist = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y);
        dist -= PHYLIB_BALL_RADIUS;

    }else if(obj2->type == PHYLIB_VCUSHION){

        dist = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x);
        dist -= PHYLIB_BALL_RADIUS;

    }else{
        return -1.0;
    }

    return dist;

}

//apply movement to a ball over a period of time
void phylib_roll(phylib_object *new, phylib_object *old, double time){

    if(new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL){
        return;
    }

    //get all the old values
    double px = old->obj.rolling_ball.pos.x, py = old->obj.rolling_ball.pos.y;
    double vx = old->obj.rolling_ball.vel.x, vy = old->obj.rolling_ball.vel.y;
    double ax = old->obj.rolling_ball.acc.x, ay = old->obj.rolling_ball.acc.y;

    //calculate the new values
    double newPx = px + (vx * time) + (0.5 * ax * time * time);
    double newPy = py + (vy * time) + (0.5 * ay * time * time);

    double newVx = vx + (ax * time);
    double newVy = vy + (ay * time);

    //update ball
    new->obj.rolling_ball.pos.x = newPx;
    new->obj.rolling_ball.pos.y = newPy;

    //check for change in sign
    if(vx * newVx <= 0){
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }else{
        new->obj.rolling_ball.vel.x = newVx;
        new->obj.rolling_ball.acc.x = ax;
    }

    if(vy * newVy <= 0){
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }else{
        new->obj.rolling_ball.vel.y = newVy;
        new->obj.rolling_ball.acc.y = ay;
    }

}

//check if a ball has stopped
unsigned char phylib_stopped(phylib_object *object){

    phylib_coord vel = object->obj.rolling_ball.vel;

    if(phylib_length(vel) < PHYLIB_VEL_EPSILON){
        unsigned char number = object->obj.rolling_ball.number;
        phylib_coord pos = object->obj.rolling_ball.pos;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = number;
        object->obj.still_ball.pos = pos;
        return 1;
    }

    return 0;

}

//apply bounce logic
void phylib_bounce(phylib_object **a, phylib_object **b){

    //define variables for switch statement
    unsigned char number;
    double length, v_rel_n, speedA, speedB;
    phylib_coord r_ab, v_rel, n, pos;

    switch((*b)->type){

        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0;
            break;
        
        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;
            break;
        
        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break;
        
        case PHYLIB_STILL_BALL:
            number = (*b)->obj.still_ball.number;
            pos = (*b)->obj.still_ball.pos;
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = number;
            (*b)->obj.rolling_ball.pos = pos;
            (*b)->obj.rolling_ball.vel = (phylib_coord){.x = 0, .y = 0};
            (*b)->obj.rolling_ball.acc = (phylib_coord){.x = 0, .y = 0};
        
        case PHYLIB_ROLLING_BALL:
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            length = phylib_length(r_ab);
            n.x = r_ab.x / length;
            n.y = r_ab.y / length;

            v_rel_n = phylib_dot_product(v_rel, n);

            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            speedA = phylib_length((*a)->obj.rolling_ball.vel);
            speedB = phylib_length((*b)->obj.rolling_ball.vel);

            if(speedA > PHYLIB_VEL_EPSILON){
                (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speedA * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speedA * PHYLIB_DRAG;
            }

            if(speedB > PHYLIB_VEL_EPSILON){
                (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speedB * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speedB * PHYLIB_DRAG;
            }

            break;
        
        default:
            return;

    }

}

//get number of rolling balls
unsigned char phylib_rolling(phylib_table *t){

    unsigned char total = 0;

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            total++;
        }

    }
    
    return total;

}

//simulate segment of time
phylib_table *phylib_segment(phylib_table *table){

    //return if max time is reached
    if(table->time >= PHYLIB_MAX_TIME){
        return NULL;
    }

    unsigned char numRoll = phylib_rolling(table);

    //return if no rolling balls
    if(numRoll == 0){
        return NULL;
    }

    table = phylib_copy_table(table);

    //loop over time
    while(table->time < PHYLIB_MAX_TIME){

        //update time
        table->time += PHYLIB_SIM_RATE;

        //loop over objects
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

            if(table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL){

                //create a copy of the ball and make it roll
                phylib_object *ball = table->object[i];
                phylib_object *newBall = NULL;
                phylib_copy_object(&newBall, &ball);

                phylib_roll(newBall, ball, PHYLIB_SIM_RATE);
                table->object[i] = newBall;
                free(ball);

            }

        }

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

            if(table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL){

                //check if the ball stopped
                if(phylib_stopped(table->object[i])){
                    return table;
                }

                //loop over object checking for a bounce
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){

                    //skip itself
                    if(j == i){
                        continue;
                    }

                    if(table->object[j]){
                        double dist = phylib_distance(table->object[i], table->object[j]);
                        if(dist < 0.0 && dist != -1.0){
                            //apply bounce and return copy of the table
                            phylib_bounce(&table->object[i], &table->object[j]);
                            return table;
                        }
                    }

                }
            }
        }

        //check for rolling balls
        if(phylib_rolling(table) == 0){
            return NULL;
        }

    }

    return table;

}

//Generate string from phylib object
char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf( string, 80,
        "STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf( string, 80,
        "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
        object->obj.rolling_ball.number,
        object->obj.rolling_ball.pos.x,
        object->obj.rolling_ball.pos.y,
        object->obj.rolling_ball.vel.x,
        object->obj.rolling_ball.vel.y,
        object->obj.rolling_ball.acc.x,
        object->obj.rolling_ball.acc.y );
        break;
    case PHYLIB_HOLE:
        snprintf( string, 80,
        "HOLE (%6.1lf,%6.1lf)",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
        break;
    case PHYLIB_HCUSHION:
        snprintf( string, 80,
        "HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
        break;
    case PHYLIB_VCUSHION:
        snprintf( string, 80,
        "VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
    }
    return string;
}
