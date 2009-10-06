/**
 * Autogenerated by Thrift
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 */
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.util.Collections;
import org.apache.log4j.Logger;

import org.apache.thrift.*;
import org.apache.thrift.meta_data.*;
import org.apache.thrift.protocol.*;

public class EqComparison implements TBase, java.io.Serializable, Cloneable, Comparable<EqComparison> {
  private static final TStruct STRUCT_DESC = new TStruct("EqComparison");
  private static final TField EQ_FIELD_DESC = new TField("eq", TType.I32, (short)1);
  private static final TField LHS_FIELD_DESC = new TField("lhs", TType.STRUCT, (short)2);
  private static final TField RHS_FIELD_DESC = new TField("rhs", TType.STRUCT, (short)3);

  /**
   * 
   * @see Equality
   */
  public int eq;
  public static final int EQ = 1;
  public Target lhs;
  public static final int LHS = 2;
  public Target rhs;
  public static final int RHS = 3;

  private final Isset __isset = new Isset();
  private static final class Isset implements java.io.Serializable {
    public boolean eq = false;
  }

  public static final Map<Integer, FieldMetaData> metaDataMap = Collections.unmodifiableMap(new HashMap<Integer, FieldMetaData>() {{
    put(EQ, new FieldMetaData("eq", TFieldRequirementType.DEFAULT, 
        new FieldValueMetaData(TType.I32)));
    put(LHS, new FieldMetaData("lhs", TFieldRequirementType.DEFAULT, 
        new StructMetaData(TType.STRUCT, Target.class)));
    put(RHS, new FieldMetaData("rhs", TFieldRequirementType.DEFAULT, 
        new StructMetaData(TType.STRUCT, Target.class)));
  }});

  static {
    FieldMetaData.addStructMetaDataMap(EqComparison.class, metaDataMap);
  }

  public EqComparison() {
  }

  public EqComparison(
    int eq,
    Target lhs,
    Target rhs)
  {
    this();
    this.eq = eq;
    this.__isset.eq = true;
    this.lhs = lhs;
    this.rhs = rhs;
  }

  /**
   * Performs a deep copy on <i>other</i>.
   */
  public EqComparison(EqComparison other) {
    __isset.eq = other.__isset.eq;
    this.eq = other.eq;
    if (other.isSetLhs()) {
      this.lhs = new Target(other.lhs);
    }
    if (other.isSetRhs()) {
      this.rhs = new Target(other.rhs);
    }
  }

  @Override
  public EqComparison clone() {
    return new EqComparison(this);
  }

  /**
   * 
   * @see Equality
   */
  public int getEq() {
    return this.eq;
  }

  /**
   * 
   * @see Equality
   */
  public EqComparison setEq(int eq) {
    this.eq = eq;
    this.__isset.eq = true;
    return this;
  }

  public void unsetEq() {
    this.__isset.eq = false;
  }

  // Returns true if field eq is set (has been asigned a value) and false otherwise
  public boolean isSetEq() {
    return this.__isset.eq;
  }

  public void setEqIsSet(boolean value) {
    this.__isset.eq = value;
  }

  public Target getLhs() {
    return this.lhs;
  }

  public EqComparison setLhs(Target lhs) {
    this.lhs = lhs;
    return this;
  }

  public void unsetLhs() {
    this.lhs = null;
  }

  // Returns true if field lhs is set (has been asigned a value) and false otherwise
  public boolean isSetLhs() {
    return this.lhs != null;
  }

  public void setLhsIsSet(boolean value) {
    if (!value) {
      this.lhs = null;
    }
  }

  public Target getRhs() {
    return this.rhs;
  }

  public EqComparison setRhs(Target rhs) {
    this.rhs = rhs;
    return this;
  }

  public void unsetRhs() {
    this.rhs = null;
  }

  // Returns true if field rhs is set (has been asigned a value) and false otherwise
  public boolean isSetRhs() {
    return this.rhs != null;
  }

  public void setRhsIsSet(boolean value) {
    if (!value) {
      this.rhs = null;
    }
  }

  public void setFieldValue(int fieldID, Object value) {
    switch (fieldID) {
    case EQ:
      if (value == null) {
        unsetEq();
      } else {
        setEq((Integer)value);
      }
      break;

    case LHS:
      if (value == null) {
        unsetLhs();
      } else {
        setLhs((Target)value);
      }
      break;

    case RHS:
      if (value == null) {
        unsetRhs();
      } else {
        setRhs((Target)value);
      }
      break;

    default:
      throw new IllegalArgumentException("Field " + fieldID + " doesn't exist!");
    }
  }

  public Object getFieldValue(int fieldID) {
    switch (fieldID) {
    case EQ:
      return getEq();

    case LHS:
      return getLhs();

    case RHS:
      return getRhs();

    default:
      throw new IllegalArgumentException("Field " + fieldID + " doesn't exist!");
    }
  }

  // Returns true if field corresponding to fieldID is set (has been asigned a value) and false otherwise
  public boolean isSet(int fieldID) {
    switch (fieldID) {
    case EQ:
      return isSetEq();
    case LHS:
      return isSetLhs();
    case RHS:
      return isSetRhs();
    default:
      throw new IllegalArgumentException("Field " + fieldID + " doesn't exist!");
    }
  }

  @Override
  public boolean equals(Object that) {
    if (that == null)
      return false;
    if (that instanceof EqComparison)
      return this.equals((EqComparison)that);
    return false;
  }

  public boolean equals(EqComparison that) {
    if (that == null)
      return false;

    boolean this_present_eq = true;
    boolean that_present_eq = true;
    if (this_present_eq || that_present_eq) {
      if (!(this_present_eq && that_present_eq))
        return false;
      if (this.eq != that.eq)
        return false;
    }

    boolean this_present_lhs = true && this.isSetLhs();
    boolean that_present_lhs = true && that.isSetLhs();
    if (this_present_lhs || that_present_lhs) {
      if (!(this_present_lhs && that_present_lhs))
        return false;
      if (!this.lhs.equals(that.lhs))
        return false;
    }

    boolean this_present_rhs = true && this.isSetRhs();
    boolean that_present_rhs = true && that.isSetRhs();
    if (this_present_rhs || that_present_rhs) {
      if (!(this_present_rhs && that_present_rhs))
        return false;
      if (!this.rhs.equals(that.rhs))
        return false;
    }

    return true;
  }

  @Override
  public int hashCode() {
    return 0;
  }

  public int compareTo(EqComparison other) {
    if (!getClass().equals(other.getClass())) {
      return getClass().getName().compareTo(other.getClass().getName());
    }

    int lastComparison = 0;
    EqComparison typedOther = (EqComparison)other;

    lastComparison = Boolean.valueOf(isSetEq()).compareTo(isSetEq());
    if (lastComparison != 0) {
      return lastComparison;
    }
    lastComparison = TBaseHelper.compareTo(eq, typedOther.eq);
    if (lastComparison != 0) {
      return lastComparison;
    }
    lastComparison = Boolean.valueOf(isSetLhs()).compareTo(isSetLhs());
    if (lastComparison != 0) {
      return lastComparison;
    }
    lastComparison = TBaseHelper.compareTo(lhs, typedOther.lhs);
    if (lastComparison != 0) {
      return lastComparison;
    }
    lastComparison = Boolean.valueOf(isSetRhs()).compareTo(isSetRhs());
    if (lastComparison != 0) {
      return lastComparison;
    }
    lastComparison = TBaseHelper.compareTo(rhs, typedOther.rhs);
    if (lastComparison != 0) {
      return lastComparison;
    }
    return 0;
  }

  public void read(TProtocol iprot) throws TException {
    TField field;
    iprot.readStructBegin();
    while (true)
    {
      field = iprot.readFieldBegin();
      if (field.type == TType.STOP) { 
        break;
      }
      switch (field.id)
      {
        case EQ:
          if (field.type == TType.I32) {
            this.eq = iprot.readI32();
            this.__isset.eq = true;
          } else { 
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case LHS:
          if (field.type == TType.STRUCT) {
            this.lhs = new Target();
            this.lhs.read(iprot);
          } else { 
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case RHS:
          if (field.type == TType.STRUCT) {
            this.rhs = new Target();
            this.rhs.read(iprot);
          } else { 
            TProtocolUtil.skip(iprot, field.type);
          }
          break;
        default:
          TProtocolUtil.skip(iprot, field.type);
          break;
      }
      iprot.readFieldEnd();
    }
    iprot.readStructEnd();


    // check for required fields of primitive type, which can't be checked in the validate method
    validate();
  }

  public void write(TProtocol oprot) throws TException {
    validate();

    oprot.writeStructBegin(STRUCT_DESC);
    oprot.writeFieldBegin(EQ_FIELD_DESC);
    oprot.writeI32(this.eq);
    oprot.writeFieldEnd();
    if (this.lhs != null) {
      oprot.writeFieldBegin(LHS_FIELD_DESC);
      this.lhs.write(oprot);
      oprot.writeFieldEnd();
    }
    if (this.rhs != null) {
      oprot.writeFieldBegin(RHS_FIELD_DESC);
      this.rhs.write(oprot);
      oprot.writeFieldEnd();
    }
    oprot.writeFieldStop();
    oprot.writeStructEnd();
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder("EqComparison(");
    boolean first = true;

    sb.append("eq:");
    String eq_name = Equality.VALUES_TO_NAMES.get(this.eq);
    if (eq_name != null) {
      sb.append(eq_name);
      sb.append(" (");
    }
    sb.append(this.eq);
    if (eq_name != null) {
      sb.append(")");
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("lhs:");
    if (this.lhs == null) {
      sb.append("null");
    } else {
      sb.append(this.lhs);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("rhs:");
    if (this.rhs == null) {
      sb.append("null");
    } else {
      sb.append(this.rhs);
    }
    first = false;
    sb.append(")");
    return sb.toString();
  }

  public void validate() throws TException {
    // check for required fields
    // check that fields of type enum have valid values
    if (isSetEq() && !Equality.VALID_VALUES.contains(eq)){
      throw new TProtocolException("The field 'eq' has been assigned the invalid value " + eq);
    }
  }

}

